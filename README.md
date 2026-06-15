# 📄 Doc QA Chatbot

A production-style RAG-powered document Q&A chatbot built with Python, Groq LLM, and ChromaDB.

## 🏗️ Project Status
- [x] Milestone 1 — LLM Chat with conversation history
- [ ] Milestone 2 — PDF ingestion & chunking
- [ ] Milestone 3 — Embeddings & vector store
- [ ] Milestone 4 — Full RAG chain + FastAPI
- [ ] Milestone 5 — Streamlit UI + Docker + Deploy

## 🚀 Quick Start

### 1. Clone & setup
```bash
git clone <your-repo-url>
cd doc-qa-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Run
```bash
python main.py
```

## 🧠 Tech Stack
| Layer | Technology |
|---|---|
| LLM | Groq (llama-3.1-8b-instant) |
| Vector DB | ChromaDB (coming M3) |
| Backend API | FastAPI (coming M4) |
| UI | Streamlit (coming M5) |

## 📁 Project Structure
```
doc-qa-chatbot/
├── src/
│   ├── config.py        # Central config from env vars
│   ├── llm.py           # LLM client wrapper (swappable)
│   └── chat.py          # Conversation history manager
├── main.py              # CLI chatbot entry point
├── requirements.txt
└── .env.example
```