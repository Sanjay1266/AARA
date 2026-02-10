from typing import List, Dict


class CitationMatcher:
    """
    Decides whether a citation should be added
    based on similarity search results.
    """

    def __init__(self, similarity_threshold: float = 0.75):
        self.similarity_threshold = similarity_threshold
        self.recent_references = []

    def decide(self, similarity_results: List[Dict]) -> Dict:
        """
        Decide citation based on similarity results.
        """

        valid = [
            r for r in similarity_results
            if r.get("similarity_score", 0) >= self.similarity_threshold
        ]

        if not valid:
            return self._no_citation("No match above threshold")

        valid.sort(key=lambda x: x["similarity_score"], reverse=True)

        best = valid[0]
        ref_id = best["reference_id"]

        return {
            "citation_required": True,
            "reference_id": ref_id,
            "confidence_score": round(best["similarity_score"], 3),
            "reason": "Best semantic match"
        }

    @staticmethod
    def _no_citation(reason: str) -> Dict:
        return {
            "citation_required": False,
            "reference_id": None,
            "confidence_score": 0.0,
            "reason": reason
        }
