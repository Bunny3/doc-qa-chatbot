# src/vectorstore/embedder.py
from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Wraps a local embedding model so it's swappable later
    (e.g. -> OpenAI embeddings, Cohere, etc.) without touching other code.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"🔢 Loading embedding model: {model_name} (first run downloads it)")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"  ✅ Model loaded. Embedding dimension: {self.dimension}")

    def embed_text(self, text: str) -> list[float]:
        """Embed a single string."""
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple strings at once — much faster than one-by-one."""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()