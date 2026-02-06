from typing import List, Dict, Optional


class CitationMatcher:
    """
    Applies quality rules on similarity results
    to decide whether a citation should be added.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.75,
        max_reuse_distance: int = 1
    ):
        """
        :param similarity_threshold: minimum similarity to accept citation
        :param max_reuse_distance: how many sentences before same reference can be reused
        """
        self.similarity_threshold = similarity_threshold
        self.max_reuse_distance = max_reuse_distance
        self.recent_references = []

    def match(
        self,
        similarity_results: List[Dict]
    ) -> Dict:
        """
        Decide best citation from similarity search results.

        similarity_results format:
        [
            {
                "reference_id": "...",
                "chunk_id": "...",
                "text": "...",
                "similarity_score": 0.83
            }
        ]
        """

        # Step 1: Filter by similarity threshold
        valid_results = [
            r for r in similarity_results
            if r["similarity_score"] >= self.similarity_threshold
        ]

        if not valid_results:
            return self._no_citation("No match above similarity threshold")

        # Step 2: Sort by similarity (descending)
        valid_results.sort(
            key=lambda x: x["similarity_score"],
            reverse=True
        )

        # Step 3: Avoid excessive repetition
        for result in valid_results:
            ref_id = result["reference_id"]

            if self._is_reference_allowed(ref_id):
                self._update_recent_references(ref_id)
                return {
                    "citation_required": True,
                    "reference_id": ref_id,
                    "confidence_score": round(result["similarity_score"], 3),
                    "reason": "High semantic similarity and passes quality controls"
                }

        return self._no_citation("Matches found but repetition rules blocked them")

    def _is_reference_allowed(self, reference_id: str) -> bool:
        """
        Check whether a reference can be reused based on recent history.
        """
        if reference_id not in self.recent_references:
            return True

        last_used_index = len(self.recent_references) - 1 - self.recent_references[::-1].index(reference_id)
        distance = len(self.recent_references) - 1 - last_used_index

        return distance >= self.max_reuse_distance

    def _update_recent_references(self, reference_id: str):
        """
        Track recently used references.
        """
        self.recent_references.append(reference_id)

        # Keep history short
        if len(self.recent_references) > 20:
            self.recent_references.pop(0)

    @staticmethod
    def _no_citation(reason: str) -> Dict:
        """
        Return standardized no-citation response.
        """
        return {
            "citation_required": False,
            "reference_id": None,
            "confidence_score": 0.0,
            "reason": reason
        }
