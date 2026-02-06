from backend.embedder import EmbeddingEngine

def main():
    chunks = [
        {
            "reference_id": "paper1.pdf",
            "chunk_id": "paper1_chunk_0",
            "text": "Neural networks are widely used in deep learning."
        },
        {
            "reference_id": "paper2.pdf",
            "chunk_id": "paper2_chunk_0",
            "text": "Climate change is caused by greenhouse gas emissions."
        },
        {
            "reference_id": "paper3.pdf",
            "chunk_id": "paper3_chunk_0",
            "text": "Machine learning enables systems to learn from data."
        }
    ]

    engine = EmbeddingEngine()
    engine.build_index(chunks)

    query = "Deep learning models use neural networks"
    results = engine.search(query)

    print("\n=== SIMILARITY RESULTS ===\n")
    for r in results:
        print("Reference :", r["reference_id"])
        print("Score     :", round(r["similarity_score"], 3))
        print("Text      :", r["text"])
        print("-" * 50)

if __name__ == "__main__":
    main()
