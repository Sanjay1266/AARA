from typing import List, Dict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    """
    Generates embeddings for text chunks
    and performs similarity search using FAISS.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunk_metadata = []

    def build_index(self, chunks: List[Dict]):
        """
        Build FAISS index from chunk texts.

        chunks format:
        [
            {
                "reference_id": "...",
                "chunk_id": "...",
                "text": "..."
            }
        ]
        """
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        # Normalize embeddings for cosine similarity
        embeddings = self._normalize(embeddings)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        self.chunk_metadata = chunks

    def search(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Search for most similar chunks to the query text.
        """
        if self.index is None:
            raise RuntimeError("FAISS index not built")

        query_embedding = self.model.encode(
            [query_text],
            convert_to_numpy=True
        )

        query_embedding = self._normalize(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.chunk_metadata[idx]
            results.append({
                "reference_id": chunk["reference_id"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "similarity_score": float(score)
            })

        return results

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms
