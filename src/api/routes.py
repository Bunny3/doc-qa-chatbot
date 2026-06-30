# src/api/routes.py
from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    ChatRequest, ChatResponse, SourceInfo,
    IngestRequest, IngestResponse,
)
from src.ingestion.pipeline import IngestionPipeline
from src.vectorstore.embedder import Embedder
from src.vectorstore.store import VectorStore
from src.llm import LLMClient
from src.rag_chain import RAGChain

router = APIRouter()

# Build shared components ONCE at module load time, not per-request.
# Loading the embedding model on every request would be very slow.
_embedder = Embedder()
_vector_store = VectorStore(embedder=_embedder)
_llm = LLMClient()
_rag_chain = RAGChain(vector_store=_vector_store, llm_client=_llm)
_ingestion_pipeline = IngestionPipeline(chunk_size=500, chunk_overlap=50)


@router.post("/ingest", response_model=IngestResponse)
def ingest_document(request: IngestRequest):
    """
    Ingest a PDF: load -> chunk -> embed -> store.
    This is the slow, one-time path — called when a new document is added.
    """
    try:
        chunks = _ingestion_pipeline.run(pdf_path=request.pdf_path)
        _vector_store.add_chunks(chunks)

        return IngestResponse(
            status="success",
            chunks_created=len(chunks),
            total_chunks_in_store=_vector_store.count(),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Ask a question. This is the fast, frequent path — the hot path of the API.
    """
    if _vector_store.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents ingested yet. Call /ingest first."
        )

    try:
        result = _rag_chain.ask(request.question, top_k=request.top_k)
        return ChatResponse(
            answer=result["answer"],
            sources=[SourceInfo(**s) for s in result["sources"]],
            chunks_used=result["chunks_used"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@router.get("/health")
def health_check():
    """Basic health check — useful for monitoring/load balancers later."""
    return {
        "status": "ok",
        "chunks_in_store": _vector_store.count(),
    }