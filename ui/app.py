import os
import streamlit as st

from backend.pipeline import CitationPipeline
from backend.docx_handler import DocxHandler


# ------------------------------
# App Config
# ------------------------------
st.set_page_config(
    page_title="Automatic Reference Adder",
    layout="centered"
)

st.title("📚 Automatic Reference Adder")
st.write("Upload a Word document and reference PDFs to generate citations automatically.")

BASE_STORAGE = "storage"
DOCX_DIR = os.path.join(BASE_STORAGE, "uploaded_docs")
PDF_DIR = os.path.join(BASE_STORAGE, "uploaded_pdfs")
OUTPUT_DIR = "output"

os.makedirs(DOCX_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------
# UI Inputs
# ------------------------------
uploaded_docx = st.file_uploader(
    "Upload Word Document (.docx)",
    type=["docx"]
)

uploaded_pdfs = st.file_uploader(
    "Upload Reference PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

citation_style = st.selectbox(
    "Select Citation Style",
    ["APA", "IEEE", "MLA"]
)

process_btn = st.button("🚀 Generate Citations")


# ------------------------------
# Processing
# ------------------------------
if process_btn:
    if not uploaded_docx or not uploaded_pdfs:
        st.error("Please upload both DOCX and at least one PDF.")
    else:
        with st.spinner("Processing documents..."):

            # Save DOCX
            docx_path = os.path.join(DOCX_DIR, uploaded_docx.name)
            with open(docx_path, "wb") as f:
                f.write(uploaded_docx.read())

            # Save PDFs
            pdf_paths = []
            for pdf in uploaded_pdfs:
                pdf_path = os.path.join(PDF_DIR, pdf.name)
                with open(pdf_path, "wb") as f:
                    f.write(pdf.read())
                pdf_paths.append(pdf_path)

            # Run pipeline
            pipeline = CitationPipeline(similarity_threshold=0.75)
            temp_output = os.path.join(OUTPUT_DIR, "with_markers.docx")

            pipeline.run(
                input_docx=docx_path,
                reference_pdfs=pdf_paths,
                output_docx=temp_output
            )

            # --- Temporary metadata (can be replaced by GROBID later)
            reference_metadata = {}
            for i, pdf in enumerate(uploaded_pdfs, start=1):
                reference_metadata[pdf.name] = {
                    "authors": ["Unknown Author"],
                    "year": "n.d.",
                    "title": pdf.name.replace(".pdf", ""),
                    "source": "User Provided PDF"
                }

            # Finalize document
            final_output = os.path.join(
                OUTPUT_DIR,
                f"cited_{uploaded_docx.name}"
            )

            handler = DocxHandler()
            handler.finalize_document(
                input_docx=temp_output,
                output_docx=final_output,
                reference_metadata=reference_metadata,
                citation_style=citation_style
            )

        st.success("✅ Citations generated successfully!")

        with open(final_output, "rb") as f:
            st.download_button(
                label="⬇️ Download Final Document",
                data=f,
                file_name=f"cited_{uploaded_docx.name}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
