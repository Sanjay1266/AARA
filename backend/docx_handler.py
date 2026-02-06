from typing import List, Dict
from docx import Document
from docx.shared import Pt


class DocxHandler:
    """
    Handles reading and writing of Word documents:
    - Extracts text
    - Inserts in-text citations
    - Appends bibliography
    """

    def __init__(self, citation_style: str = "APA"):
        self.citation_style = citation_style

    # --------------------------------------------------
    # READ
    # --------------------------------------------------
    def extract_paragraphs(self, docx_path: str) -> List[str]:
        """
        Extract paragraphs from a DOCX file.
        """
        document = Document(docx_path)
        paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        return paragraphs

    # --------------------------------------------------
    # WRITE
    # --------------------------------------------------
    def insert_citations(
        self,
        input_docx: str,
        output_docx: str,
        citation_map: Dict[int, str],
        bibliography_entries: List[str]
    ):
        """
        Insert citations into the document and append bibliography.

        citation_map:
        {
            paragraph_index: "(Smith et al., 2021)"
        }
        """
        document = Document(input_docx)

        # Insert in-text citations
        for idx, paragraph in enumerate(document.paragraphs):
            if idx in citation_map:
                citation_text = citation_map[idx]
                run = paragraph.add_run(f" {citation_text}")
                run.font.size = Pt(11)

        # Append bibliography
        self._append_bibliography(document, bibliography_entries)

        document.save(output_docx)

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------
    def _append_bibliography(self, document: Document, entries: List[str]):
        """
        Add bibliography section at the end of the document.
        """
        document.add_page_break()

        heading = document.add_heading("References", level=1)
        heading.alignment = 0  # left align

        for entry in entries:
            p = document.add_paragraph(entry)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.left_indent = Pt(18)
