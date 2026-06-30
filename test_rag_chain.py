# test_rag_chain.py
from src.vectorstore.embedder import Embedder
from src.vectorstore.store import VectorStore
from src.llm import LLMClient
from src.rag_chain import RAGChain


def main():
    embedder = Embedder()
    store = VectorStore(embedder=embedder)
    llm = LLMClient()
    rag = RAGChain(vector_store=store, llm_client=llm)

    print(f"\n📦 Vector store has {store.count()} chunks\n")

    questions = [
        "What is self-attention?",
        "What dataset was used for training?",
        "What is the capital of France?",  # should say "I don't know" - not in doc
    ]

    for q in questions:
        print(f"\n❓ Question: {q}")
        result = rag.ask(q)
        print(f"💬 Answer: {result['answer']}")
        print(f"📎 Sources: {result['sources']}")
        print(f"📦 Chunks used: {result['chunks_used']}")


if __name__ == "__main__":
    main()