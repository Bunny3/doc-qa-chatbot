# src/ingestion/chunker.py
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.get_encoding("cl100k_base")

        # RecursiveCharacterTextSplitter tries to split on:
        # paragraphs → sentences → words → characters (in that order)
        # This preserves meaning better than fixed-size splitting
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=self._count_tokens,  # measure in tokens, not chars
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def _count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def chunk_pages(self, pages: list[dict]) -> list[dict]:
        """
        Takes page dicts from PDFLoader and returns chunk dicts:
        {
            "chunk_index": 0,
            "text": "chunk content...",
            "token_count": 487,
            "source": "filename.pdf",
            "page_number": 3,
        }
        """
        all_chunks = []
        chunk_index = 0

        for page in pages:
            splits = self.splitter.split_text(page["text"])

            for split in splits:
                token_count = self._count_tokens(split)

                all_chunks.append({
                    "chunk_index": chunk_index,
                    "text": split,
                    "token_count": token_count,
                    "source": page["source"],
                    "page_number": page["page_number"],
                })
                chunk_index += 1

        return all_chunks

    def print_stats(self, chunks: list[dict]):
        """Useful for debugging chunk quality."""
        token_counts = [c["token_count"] for c in chunks]
        print(f"\n📊 Chunking Stats:")
        print(f"   Total chunks : {len(chunks)}")
        print(f"   Avg tokens   : {sum(token_counts) // len(token_counts)}")
        print(f"   Min tokens   : {min(token_counts)}")
        print(f"   Max tokens   : {max(token_counts)}")