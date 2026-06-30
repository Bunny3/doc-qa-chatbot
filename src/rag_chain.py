# src/rag_chain.py
from src.llm import LLMClient
from src.vectorstore.store import VectorStore

RAG_SYSTEM_PROMPT = """You are a document Q&A assistant. Use the context below to answer the user's question as helpfully as possible.

Guidelines:
- Base your answer on the context provided. You may synthesize and explain ideas
  using the context, not just copy it verbatim.
- Some context chunks may be irrelevant or contain noisy/garbled text (e.g. from
  figures or tables) — ignore those and use whatever chunks ARE relevant.
- If the context says "No relevant context found" or contains nothing useful to
  the question, you MUST respond with exactly: "I don't have enough information
  in the document to answer that." Do NOT use your own knowledge to answer in
  this case, even if you know the answer.
- Cite the source page when useful.

Context:
{context}
"""


class RAGChain:
    """
    Orchestrates: retrieve relevant chunks -> build grounded prompt -> generate answer.
    """

    def __init__(self, vector_store: VectorStore, llm_client: LLMClient, max_distance: float = 1.15):
        self.vector_store = vector_store
        self.llm = llm_client
        self.max_distance = max_distance

    def _format_context(self, chunks: list[dict]) -> str:
        """Turn retrieved chunks into a readable context block with source attribution."""
        if not chunks:
            return "No relevant context found."

        formatted = []
        for chunk in chunks:
            source = chunk["metadata"]["source"]
            page = chunk["metadata"]["page_number"]
            formatted.append(f"[Source: {source}, page {page}]\n{chunk['text']}")
        return "\n\n---\n\n".join(formatted)

    def ask(self, question: str, top_k: int = 3) -> dict:
        """
        Full RAG flow. Returns dict with:
        - answer: the generated response
        - sources: list of (source, page) tuples used
        - chunks_used: how many chunks were retrieved and used
        """
        # Step 1: Retrieve
        chunks = self.vector_store.search(
            question, top_k=top_k, max_distance=self.max_distance
        )

        # Step 2: Build grounded prompt
        context = self._format_context(chunks)
        system_prompt = RAG_SYSTEM_PROMPT.format(context=context)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]

        # Step 3: Generate
        answer = self.llm.chat(messages)

        sources = [
            {"source": c["metadata"]["source"], "page": c["metadata"]["page_number"]}
            for c in chunks
        ]

        return {
            "answer": answer,
            "sources": sources,
            "chunks_used": len(chunks),
        }