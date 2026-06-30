# src/api/app.py
from fastapi import FastAPI
from src.config import config
from src.api.routes import router

app = FastAPI(
    title="Doc QA Chatbot API",
    description="RAG-powered document Q&A backend",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    config.validate()
    print("🚀 API server started and ready.")