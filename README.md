# 📄 Doc QA Chatbot

A production-style RAG-powered document Q&A chatbot. Upload a PDF, ask questions, and get answers grounded in the actual document — not the model's general knowledge.

Built end-to-end: PDF ingestion → chunking → embeddings → vector search → grounded LLM generation → REST API → chat UI → Docker → live deployment.

## 🏗️ Project Status

- [x] Milestone 1 — LLM chat with conversation history
- [x] Milestone 2 — PDF ingestion & chunking
- [x] Milestone 3 — Embeddings & ChromaDB vector store
- [x] Milestone 4 — Full RAG chain + FastAPI backend
- [x] Milestone 5 — Streamlit UI + Docker + Deploy

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (llama-3.1-8b-instant) |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2, local, free) |
| Vector DB | ChromaDB |
| Backend API | FastAPI |
| UI | Streamlit |
| Containerization | Docker |
| Deployment | Render |

## 🚀 Quick Start

### 1. Clone & setup
```bash
git clone https://github.com/Bunny3/doc-qa-chatbot.git
cd doc-qa-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-ui.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Run the API
```bash
uvicorn src.api.app:app --reload --reload-dir src --port 8000
```

### 4. Run the UI (in a separate terminal)
```bash
streamlit run ui/app.py
```

### 5. Or run with Docker
```bash
docker build -t doc-qa-chatbot .
docker run -d -p 8000:8000 --env-file .env doc-qa-chatbot
```

## 📁 Project Structure
```doc-qa-chatbot/
├── src/
│   ├── config.py              # Central config from env vars
│   ├── llm.py                 # LLM client wrapper (Groq, swappable)
│   ├── chat.py                # Conversation history manager
│   ├── rag_chain.py           # Retrieval -> grounded prompt -> generation
│   ├── ingestion/
│   │   ├── pdf_loader.py      # PDF text extraction
│   │   ├── chunker.py         # Token-aware chunking with overlap
│   │   └── pipeline.py        # Orchestrates load -> chunk -> save
│   ├── vectorstore/
│   │   ├── embedder.py        # Local embeddings (SentenceTransformers)
│   │   └── store.py           # ChromaDB wrapper with similarity search
│   └── api/
│       ├── app.py             # FastAPI app entry point
│       ├── routes.py          # /chat, /ingest, /health endpoints
│       └── schemas.py         # Pydantic request/response models
├── ui/
│   └── app.py                 # Streamlit chat interface
├── seed_data/
│   └── sample.pdf             # Bundled into Docker image for demo
├── Dockerfile
├── requirements.txt           # Backend dependencies
└── requirements-ui.txt        # Streamlit-only dependencies
```
## 🔍 How It Works

1. **Ingestion** — A PDF is parsed page-by-page, cleaned, and split into ~500-token chunks with 50-token overlap to preserve context across boundaries.
2. **Embedding** — Each chunk is embedded locally using `all-MiniLM-L6-v2` (no API cost) and stored in ChromaDB with source/page metadata.
3. **Retrieval** — A user question is embedded and matched against stored chunks via cosine similarity, filtered by a calibrated distance threshold to reject weak matches.
4. **Generation** — Retrieved chunks are injected into a grounding prompt instructing the LLM to answer only from context, explicitly refusing to fall back on outside knowledge when context is empty or irrelevant.
5. **API** — FastAPI exposes `/chat`, `/ingest`, and `/health`. Heavy components (embedding model, vector store, LLM client) are initialized once at startup, not per-request.

## 🐛 Notable Bugs Found & Fixed

Real production-style debugging done along the way, not just a happy-path build:

- **Grounding failures**: an overly strict prompt caused the model to refuse answering even with relevant context present; an overly loose fix then caused it to hallucinate when context was empty. Fixed with an explicit instruction for the empty-context case specifically.
- **Chunk ID collisions**: ingesting multiple documents could silently overwrite each other's chunks since IDs were index-based only. Fixed by prefixing IDs with the source filename.
- **Non-idempotent ingestion**: `ChromaDB.add()` was duplicating chunks on re-ingestion of the same file. Fixed by switching to `.upsert()`.

## 📌 Known Limitations / Next Steps

- No deduplication check on ingest beyond filename-based upsert
- PDF table/figure extraction can produce noisy chunks (handled via distance threshold, not fixed at the source)
- Free-tier deployment has no persistent disk — vector store rebuilds from a bundled sample PDF on every cold start
- Next: swap ChromaDB for a cloud-hosted vector DB (Pinecone/Qdrant) to support multi-document, persistent production use