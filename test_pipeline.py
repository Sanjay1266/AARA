from backend.pipeline import CitationPipeline

def main():
    pipeline = CitationPipeline(similarity_threshold=0.75)

    input_docx = "sample.docx"
    reference_pdfs = [
        "sample_reference.pdf"
    ]

    output_docx = "final_with_markers.docx"

    pipeline.run(
        input_docx=input_docx,
        reference_pdfs=reference_pdfs,
        output_docx=output_docx
    )

if __name__ == "__main__":
    main()
