# src/vectorstore/store.py
import chromadb
from src.vectorstore.embedder import Embedder


class VectorStore:
    """
    Wraps ChromaDB to store chunks + their embeddings, and search by similarity.
    """

    def __init__(self, embedder: Embedder, collection_name: str = "doc_chunks", persist_dir: str = "chroma_db"):
        self.embedder = embedder
        # PersistentClient saves to disk — survives restarts (unlike in-memory)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks: list[dict]):
        """
        Takes chunk dicts from M2's pipeline and stores them with embeddings.
        Each chunk dict looks like:
        {
            "chunk_index": 0,
            "text": "...",
            "token_count": 476,
            "source": "sample.pdf",
            "page_number": 1,
        }
        """
        texts = [chunk["text"] for chunk in chunks]

        print(f"🔢 Embedding {len(texts)} chunks...")
        embeddings = self.embedder.embed_batch(texts)

        # ChromaDB needs: unique ids, embeddings, documents (raw text), metadata
        ids = [f"chunk_{c['chunk_index']}" for c in chunks]
        metadatas = [
            {
                "source": c["source"],
                "page_number": c["page_number"],
                "token_count": c["token_count"],
            }
            for c in chunks
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        print(f"  ✅ Stored {len(chunks)} chunks in ChromaDB.")

    def search(self, query: str, top_k: int = 3, max_distance: float = None) -> list[dict]:
        """
        Embed the query and find the top_k most similar chunks.
        If max_distance is set, filters out chunks that are too dissimilar
        (lower distance = more similar; this prevents returning irrelevant chunks).
        """
        query_embedding = self.embedder.embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        output = []
        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            if max_distance is not None and distance > max_distance:
                continue
            output.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": distance,
            })
        return output

    def count(self) -> int:
        return self.collection.count()