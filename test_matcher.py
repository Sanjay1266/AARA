from backend.matcher import CitationMatcher

def main():
    matcher = CitationMatcher(similarity_threshold=0.75)

    similarity_results = [
        {
            "reference_id": "paper1.pdf",
            "chunk_id": "paper1_chunk_0",
            "text": "Neural networks are widely used in deep learning.",
            "similarity_score": 0.82
        },
        {
            "reference_id": "paper2.pdf",
            "chunk_id": "paper2_chunk_3",
            "text": "Machine learning systems learn from data.",
            "similarity_score": 0.78
        },
        {
            "reference_id": "paper3.pdf",
            "chunk_id": "paper3_chunk_1",
            "text": "Unrelated content.",
            "similarity_score": 0.45
        }
    ]

    decision = matcher.match(similarity_results)

    print("\n=== MATCHER DECISION ===")
    for k, v in decision.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
