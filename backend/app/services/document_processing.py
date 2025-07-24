from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os
from typing import List
from langchain.schema import Document


def process_pdf(
    file_bytes: bytes,
    source_filename: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    add_metadata_source: bool = True,
) -> List[Document]:
    """Load PDF from bytes, split into chunks, and optionally add source metadata."""

    # Use NamedTemporaryFile with delete=False because PyPDFLoader needs path access
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " "]  # Removed empty string separator
        )
        chunks = text_splitter.split_documents(documents)

        if add_metadata_source and source_filename:
            for doc in chunks:
                doc.metadata["source"] = source_filename

        return chunks

    except Exception as e:
        # Optional: log or raise if you want caller to handle
        raise RuntimeError(f"Failed to process PDF: {e}") from e

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
