# src/ingestion/pipeline.py
import json
from pathlib import Path
from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.chunker import TextChunker


class IngestionPipeline:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunker = TextChunker(chunk_size, chunk_overlap)

    def run(self, pdf_path: str, save_to: str = None) -> list[dict]:
        """
        Full pipeline: PDF → pages → chunks → (optionally save to JSON)
        Returns list of chunk dicts.
        """
        loader = PDFLoader(pdf_path)
        pages = loader.load()

        chunks = self.chunker.chunk_pages(pages)
        self.chunker.print_stats(chunks)

        if save_to:
            output_path = Path(save_to)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(chunks, f, indent=2)
            print(f"\n💾 Chunks saved to: {output_path}")

        return chunks