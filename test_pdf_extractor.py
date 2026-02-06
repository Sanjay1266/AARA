from backend.pdf_extractor import PDFExtractor

def main():
    extractor = PDFExtractor()

    pdf_path = "sample_reference.pdf"  # put a real PDF here
    text = extractor.extract_text_from_pdf(pdf_path)

    print("\n=== EXTRACTED TEXT (first 1000 chars) ===\n")
    print(text[:1000])

    print("\n✅ PDF extraction successful")

if __name__ == "__main__":
    main()
