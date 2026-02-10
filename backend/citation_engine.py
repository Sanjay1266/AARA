class CitationEngine:
    """
    Generates in-text citations based on citation style.
    """

    def __init__(self, style: str = "APA"):
        self.style = style.upper()

    def format_in_text(self, ref_id: str, metadata: dict) -> str:
        """
        Generate in-text citation.
        """
        authors = metadata.get("authors", [])
        year = metadata.get("year", "n.d.")

        if self.style == "APA":
            if len(authors) == 0:
                return f"({ref_id}, {year})"
            elif len(authors) == 1:
                return f"({authors[0]}, {year})"
            else:
                return f"({authors[0]} et al., {year})"

        if self.style == "IEEE":
            return f"[{metadata.get('index')}]"

        if self.style == "MLA":
            return f"({authors[0]})" if authors else f"({ref_id})"

        # fallback
        return f"({ref_id}, {year})"
