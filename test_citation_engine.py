from backend.citation_engine import CitationEngine
from backend.bibliography_builder import BibliographyBuilder

def main():
    metadata = {
        "paper1.pdf": {
            "authors": ["Smith, J.", "Brown, L."],
            "year": 2021,
            "title": "Deep Learning Methods",
            "source": "Journal of AI",
            "index": 1
        }
    }

    citation_engine = CitationEngine(style="APA")
    bib_builder = BibliographyBuilder(style="APA")

    print("In-text citation:")
    print(citation_engine.format_in_text("paper1.pdf", metadata["paper1.pdf"]))

    print("\nBibliography entry:")
    print(bib_builder.build_entry("paper1.pdf", metadata["paper1.pdf"]))

if __name__ == "__main__":
    main()
