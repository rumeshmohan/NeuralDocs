from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import documents, queries
import logging

app = FastAPI(title=settings.APP_NAME)

# Setup logging (if not configured elsewhere)
logging.basicConfig(level=logging.INFO)

# Ensure CORS_ORIGINS is a list
origins = settings.CORS_ORIGINS
if isinstance(origins, str):
    origins = [origin.strip() for origin in origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(queries.router, prefix="/api/queries", tags=["queries"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "health": "ok"}
