from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
import chromadb  # optional if not creating client yourself here
from app.services.vector_store import VectorStore  # import your VectorStore class

router = APIRouter()
logger = logging.getLogger(__name__)

# Simply instantiate VectorStore normally, no `collection` argument needed
vector_store = VectorStore()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        raw_bytes = await file.read()

        # Clear existing documents from the vector store's collection before new ingestion
        # NOTE: You need a method in VectorStore to get collection and delete docs or add one
        # If not implemented, consider adding this clearing logic inside VectorStore
        existing_ids = vector_store.vector_store.get().get("ids", [])
        if existing_ids:
            vector_store.vector_store.delete(ids=existing_ids)
            logger.info(f"Cleared {len(existing_ids)} existing documents from vector store.")

        document_ids = vector_store.add_documents(raw_bytes, file.filename)

        return {"document_ids": document_ids, "uploaded_filename": file.filename}

    except Exception as e:
        logger.error(f"Document upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Document processing failed") from e
