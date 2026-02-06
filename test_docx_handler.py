from backend.docx_handler import DocxHandler

def main():
    handler = DocxHandler(citation_style="APA")

    citation_map = {
        0: "(Smith et al., 2021)",
        2: "(Johnson, 2019)"
    }

    bibliography = [
        "Smith, J., Brown, L. (2021). Deep Learning Methods. Journal of AI.",
        "Johnson, R. (2019). Machine Learning Basics. Springer."
    ]

    handler.insert_citations(
        input_docx="sample.docx",
        output_docx="output_cited.docx",
        citation_map=citation_map,
        bibliography_entries=bibliography
    )

    print("✅ DOCX citation insertion complete")

if __name__ == "__main__":
    main()
