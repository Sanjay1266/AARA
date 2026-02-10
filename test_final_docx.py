from backend.docx_handler import DocxHandler

def main():
    reference_metadata = {
        "paper1.pdf": {
            "authors": ["Smith, J.", "Brown, L."],
            "year": 2021,
            "title": "Deep Learning Methods",
            "source": "Journal of AI"
        },
        "paper2.pdf": {
            "authors": ["Johnson, R."],
            "year": 2019,
            "title": "Machine Learning Basics",
            "source": "Springer"
        }
    }

    handler = DocxHandler()

    handler.finalize_document(
        input_docx="final_with_markers.docx",
        output_docx="final_cited_document.docx",
        reference_metadata=reference_metadata,
        citation_style="APA"
    )

    print("✅ Final cited document created successfully")

if __name__ == "__main__":
    main()
