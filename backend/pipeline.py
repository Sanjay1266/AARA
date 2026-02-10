from typing import List, Dict

from backend.pdf_extractor import PDFExtractor
from backend.text_chunker import TextChunker
from backend.embedder import EmbeddingEngine
from backend.matcher import CitationMatcher
from backend.docx_handler import DocxHandler


class CitationPipeline:
    """
    Orchestrates the complete citation workflow.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.75,
        top_k: int = 5
    ):
        self.pdf_extractor = PDFExtractor()
        self.chunker = TextChunker()
        self.embedder = EmbeddingEngine()
        self.matcher = CitationMatcher(
            similarity_threshold=similarity_threshold
        )
        self.docx_handler = DocxHandler()
        self.top_k = top_k

    def run(
        self,
        input_docx: str,
        reference_pdfs: List[str],
        output_docx: str
    ):
        """
        Run the full pipeline.
        """

        # 1️⃣ Extract text from PDFs
        print("[PIPELINE] Extracting PDF text...")
        extracted_texts = self.pdf_extractor.extract_from_multiple_pdfs(
            reference_pdfs
        )

        # 2️⃣ Chunk PDF texts
        print("[PIPELINE] Chunking reference texts...")
        chunks = self.chunker.chunk_all_references(extracted_texts)

        if not chunks:
            raise RuntimeError("No valid text chunks created from PDFs")

        # 3️⃣ Build embedding index
        print("[PIPELINE] Building embedding index...")
        self.embedder.build_index(chunks)

        # 4️⃣ Read DOCX paragraphs
        print("[PIPELINE] Reading DOCX paragraphs...")
        paragraphs = self.docx_handler.read_paragraphs(input_docx)

        citation_decisions: Dict[int, Dict] = {}

        # 5️⃣ Process each paragraph
        print("[PIPELINE] Matching citations...")
        for idx, paragraph in enumerate(paragraphs):
            similarity_results = self.embedder.search(
                paragraph,
                top_k=self.top_k
            )

            decision = self.matcher.decide(similarity_results)

            if decision["citation_required"]:
                citation_decisions[idx] = decision

        # 6️⃣ Insert citation markers
        print("[PIPELINE] Writing output DOCX...")
        self.docx_handler.insert_citation_markers(
            input_docx=input_docx,
            output_docx=output_docx,
            citation_decisions=citation_decisions
        )

        print("✅ Pipeline completed successfully")
