# test_ingestion.py
from src.ingestion.pipeline import IngestionPipeline

def main():
    pipeline = IngestionPipeline(chunk_size=500, chunk_overlap=50)

    chunks = pipeline.run(
        pdf_path="data/raw/sample.pdf",
        save_to="data/processed/chunks.json"
    )

    print("\n🔍 First 3 chunks:\n")
    for chunk in chunks[:3]:
        print(f"--- Chunk {chunk['chunk_index']} "
              f"[page {chunk['page_number']}, {chunk['token_count']} tokens] ---")
        print(chunk["text"][:300])
        print()

if __name__ == "__main__":
    main()