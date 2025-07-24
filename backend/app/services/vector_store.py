from langchain_chroma import Chroma
from app.core.embeddings import get_embeddings
from app.core.config import settings
from typing import List
from langchain.schema import Document
from app.services.document_processing import process_pdf
import logging
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        try:
            self.embeddings = get_embeddings()
            self.persist_dir = settings.CHROMA_PERSIST_DIR
            os.makedirs(self.persist_dir, exist_ok=True)  # Ensure dir exists
            self.vector_store = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
            logger.info(f"Initialized Chroma vector store at {self.persist_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise

    def add_documents(self, file_bytes: bytes, filename: str) -> List[str]:
        try:
            chunks = process_pdf(file_bytes, source_filename=filename)
            ids = self.vector_store.add_documents(chunks)
            logger.info(f"Added {len(chunks)} document chunks for file {filename}")
            return ids
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise

    def query(self, query: str, k: int = 1) -> List[Document]:
        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Query executed: '{query}' with top {k} results")
            return results
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise
