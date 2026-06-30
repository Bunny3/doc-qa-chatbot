# src/api/schemas.py
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


class SourceInfo(BaseModel):
    source: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
    chunks_used: int


class IngestRequest(BaseModel):
    pdf_path: str


class IngestResponse(BaseModel):
    status: str
    chunks_created: int
    total_chunks_in_store: int