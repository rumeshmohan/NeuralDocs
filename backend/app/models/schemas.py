from pydantic import BaseModel
from typing import List, Optional

class DocumentBase(BaseModel):
    content: str
    metadata: dict

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: str

    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    query: str
    k: int = 1

class QueryResult(Document):
    score: float