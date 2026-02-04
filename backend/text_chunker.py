from typing import Dict, List
import re

import spacy

# Load spaCy model (small + fast)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "spaCy model not found. Run: python -m spacy download en_core_web_sm"
    )

class TextChunker:
    """
    Splits extracted PDF text into semantic chunks
    while preserving reference identity.
    """

    def __init__(self, max_chunk_words: int = 150, overlap_words: int = 30):
        """
        :param max_chunk_words: Maximum words per chunk
        :param overlap_words: Overlap between chunks (for context preservation)
        """
        self.max_chunk_words = max_chunk_words
        self.overlap_words = overlap_words

    def chunk_all_references(
        self, extracted_texts: Dict[str, str]
    ) -> List[Dict]:
        """
        Chunk text from multiple PDFs.

        Input:
        {
            "paper1.pdf": "full extracted text...",
            "paper2.pdf": "full extracted text..."
        }

        Output:
        [
            {
                "reference_id": "paper1.pdf",
                "chunk_id": "paper1.pdf_chunk_0",
                "text": "chunk text ..."
            },
            ...
        ]
        """
        all_chunks = []

        for reference_id, text in extracted_texts.items():
            if not text.strip():
                continue

            chunks = self._chunk_single_text(text)

            for idx, chunk in enumerate(chunks):
                all_chunks.append({
                    "reference_id": reference_id,
                    "chunk_id": f"{reference_id}_chunk_{idx}",
                    "text": chunk
                })

        return all_chunks

    def _chunk_single_text(self, text: str) -> List[str]:
        """
        Chunk a single document text into semantic chunks.
        """
        text = self._clean_text(text)

        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        chunks = []
        current_chunk = []
        current_word_count = 0

        for sentence in sentences:
            sentence_word_count = len(sentence.split())

            # If adding sentence exceeds chunk size → finalize chunk
            if current_word_count + sentence_word_count > self.max_chunk_words:
                chunks.append(" ".join(current_chunk))

                # Start new chunk with overlap
                if self.overlap_words > 0:
                    overlap = self._get_overlap_words(current_chunk)
                    current_chunk = overlap.copy()
                    current_word_count = len(" ".join(current_chunk).split())
                else:
                    current_chunk = []
                    current_word_count = 0

            current_chunk.append(sentence)
            current_word_count += sentence_word_count

        # Add remaining chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _get_overlap_words(self, chunk_sentences: List[str]) -> List[str]:
        """
        Returns last N words as overlap sentences.
        """
        words = " ".join(chunk_sentences).split()
        overlap_words = words[-self.overlap_words:]

        if not overlap_words:
            return []

        return [" ".join(overlap_words)]

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Light normalization for chunking.
        """
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\x00", "")
        return text.strip()
