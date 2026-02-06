from backend.text_chunker import TextChunker

def main():
    # Sample extracted PDF texts (simulate output of pdf_extractor)
    extracted_texts = {
        "paper1.pdf": (
            "Machine learning is a subset of artificial intelligence. "
            "It enables systems to learn from data without explicit programming. "
            "Neural networks are widely used in deep learning applications. "
            "Convolutional neural networks are effective for image processing. "
            "Recurrent neural networks are suitable for sequence modeling. "
            "Transformers have recently outperformed traditional models."
        ),
        "paper2.pdf": (
            "Climate change refers to long-term shifts in temperatures. "
            "These shifts may be natural or human-induced. "
            "Greenhouse gas emissions are a major cause of global warming. "
            "Renewable energy can reduce carbon emissions significantly."
        )
    }

    # Initialize chunker
    chunker = TextChunker(
        max_chunk_words=20,   # small size to force chunking
        overlap_words=5
    )

    # Chunk texts
    chunks = chunker.chunk_all_references(extracted_texts)

    # Display results
    print("\n=== CHUNKING RESULTS ===\n")
    for chunk in chunks:
        print(f"Reference ID : {chunk['reference_id']}")
        print(f"Chunk ID     : {chunk['chunk_id']}")
        print(f"Text         : {chunk['text']}")
        print(f"Word count   : {len(chunk['text'].split())}")
        print("-" * 50)

    print(f"\nTotal chunks created: {len(chunks)}")


if __name__ == "__main__":
    main()
