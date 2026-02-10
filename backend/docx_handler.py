import re
from typing import Dict
from docx import Document
from docx.shared import Pt

from backend.citation_engine import CitationEngine
from backend.bibliography_builder import BibliographyBuilder


class DocxHandler:
    """
    Handles final DOCX processing:
    - Replace citation markers with formatted citations
    - Append bibliography section
    """

    CITE_PATTERN = re.compile(r"\[CITE:\s*(.*?)\s*\|\s*(.*?)\]")

    def finalize_document(
        self,
        input_docx: str,
        output_docx: str,
        reference_metadata: Dict[str, Dict],
        citation_style: str = "APA"
    ):
        document = Document(input_docx)

        citation_engine = CitationEngine(style=citation_style)
        bibliography_builder = BibliographyBuilder(style=citation_style)

        used_references = []

        # 🔹 Replace markers with formatted citations
        for paragraph in document.paragraphs:
            matches = list(self.CITE_PATTERN.finditer(paragraph.text))
            if not matches:
                continue

            new_text = paragraph.text

            for match in matches:
                ref_id = match.group(1).strip()

                if ref_id not in reference_metadata:
                    continue

                citation_text = citation_engine.format_in_text(
                    ref_id, reference_metadata[ref_id]
                )

                new_text = new_text.replace(match.group(0), citation_text)

                if ref_id not in used_references:
                    used_references.append(ref_id)

            paragraph.clear()
            run = paragraph.add_run(new_text)
            run.font.size = Pt(11)

        # 🔹 Append bibliography
        self._append_bibliography(
            document,
            used_references,
            reference_metadata,
            bibliography_builder
        )

        document.save(output_docx)

    def _append_bibliography(
        self,
        document: Document,
        used_references,
        reference_metadata,
        bibliography_builder
    ):
        document.add_page_break()
        document.add_heading("References", level=1)

        for idx, ref_id in enumerate(used_references, start=1):
            metadata = reference_metadata[ref_id].copy()
            metadata["index"] = idx

            entry = bibliography_builder.build_entry(ref_id, metadata)
            p = document.add_paragraph(entry)
            p.paragraph_format.space_after = Pt(6)
