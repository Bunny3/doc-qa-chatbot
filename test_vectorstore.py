# test_vectorstore.py
import json
from src.vectorstore.embedder import Embedder
from src.vectorstore.store import VectorStore


def main():
    # Load chunks from M2
    with open("data/processed/chunks.json") as f:
        chunks = json.load(f)

    print(f"📦 Loaded {len(chunks)} chunks from M2\n")

    # Build embedder + vector store
    embedder = Embedder()
    store = VectorStore(embedder=embedder)

    # Only embed if store is empty (avoid re-embedding every run)
    if store.count() == 0:
        store.add_chunks(chunks)
    else:
        print(f"ℹ️  Vector store already has {store.count()} chunks, skipping embed.")

    # Test queries
    test_queries = [
        "What is self-attention?",
        "How does the Transformer architecture work?",
        "What dataset was used for training?",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        results = store.search(query, top_k=3, max_distance=1.15)
        for i, r in enumerate(results, 1):
            print(f"  [{i}] (distance={r['distance']:.4f}, page={r['metadata']['page_number']})")
            print(f"      {r['text'][:150]}...")


if __name__ == "__main__":
    main()