from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RAG API"
    CORS_ORIGINS: list = ["http://localhost:5173"]
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()