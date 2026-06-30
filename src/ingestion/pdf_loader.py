# src/ingestion/pdf_loader.py
import re
from pathlib import Path
from pypdf import PdfReader


class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")
        if self.file_path.suffix.lower() != ".pdf":
            raise ValueError(f"File must be a PDF: {file_path}")

    def load(self) -> list[dict]:
        """
        Returns a list of pages, each as a dict:
        {
            "page_number": 1,
            "text": "raw text from page...",
            "source": "filename.pdf"
        }
        """
        reader = PdfReader(self.file_path)
        pages = []

        print(f"📄 Loading: {self.file_path.name} ({len(reader.pages)} pages)")

        for page_num, page in enumerate(reader.pages, start=1):
            raw_text = page.extract_text()

            if not raw_text or not raw_text.strip():
                print(f"  ⚠️  Page {page_num} is empty or unreadable, skipping.")
                continue

            cleaned = self._clean_text(raw_text)

            pages.append({
                "page_number": page_num,
                "text": cleaned,
                "source": self.file_path.name,
            })

        print(f"  ✅ Extracted {len(pages)} pages successfully.")
        return pages

    def _clean_text(self, text: str) -> str:
        """Remove noise common in PDF extraction."""
        text = re.sub(r'\n{3,}', '\n\n', text)   # collapse extra newlines
        text = re.sub(r'-\n', '', text)          # fix hyphenated line breaks
        text = re.sub(r' {2,}', ' ', text)       # collapse extra spaces
        return text.strip()