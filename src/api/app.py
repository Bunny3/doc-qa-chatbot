# src/api/app.py
from fastapi import FastAPI
from src.config import config
from src.api.routes import router, _ingestion_pipeline, _vector_store

app = FastAPI(
    title="Doc QA Chatbot API",
    description="RAG-powered document Q&A backend",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    config.validate()

    # Auto-ingest the sample PDF on startup since Render's free tier
    # doesn't persist disk between restarts/cold starts
    if _vector_store.count() == 0:
        print("📄 Auto-ingesting sample.pdf on startup...")
        chunks = _ingestion_pipeline.run(pdf_path="data/raw/sample.pdf")
        _vector_store.add_chunks(chunks)

    print("🚀 API server started and ready.")