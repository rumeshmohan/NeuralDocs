from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest
from app.services.vector_store import VectorStore
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize VectorStore once to maintain connection and collection reuse
vector_store = VectorStore()

@router.post("/")
async def query_documents(request: QueryRequest):
    try:
        # Assuming vector_store.query receives (query_text: str, k: int)
        results = vector_store.query(request.query, request.k)
        return {"results": results}
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Query execution failed") from e
