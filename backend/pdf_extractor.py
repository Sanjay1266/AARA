import os
from typing import Dict, List

import fitz  # PyMuPDF
import pdfplumber


class PDFExtractor:
    """
    Extracts text from PDF files.
    Works for text-based PDFs.
    """

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a single PDF file.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        text_parts = []

        # -------- Method 1: PyMuPDF (fast) --------
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text_parts.append(page_text)
        except Exception:
            pass

        # -------- Method 2: pdfplumber (fallback) --------
        if len(" ".join(text_parts).strip()) < 300:
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
            except Exception:
                pass

        return self._clean_text("\n".join(text_parts))

    def extract_from_multiple_pdfs(
        self, pdf_paths: List[str]
    ) -> Dict[str, str]:
        """
        Extract text from multiple PDFs.
        Returns:
        {
            "paper1.pdf": "extracted text...",
            "paper2.pdf": "extracted text..."
        }
        """
        extracted = {}

        for path in pdf_paths:
            filename = os.path.basename(path)
            try:
                extracted[filename] = self.extract_text_from_pdf(path)
            except Exception as e:
                print(f"[ERROR] {filename}: {e}")
                extracted[filename] = ""

        return extracted

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Basic text cleanup.
        """
        text = text.replace("\x00", " ")
        text = " ".join(text.split())
        return text.strip()
