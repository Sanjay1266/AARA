class BibliographyBuilder:
    """
    Builds bibliography entries based on citation style.
    """

    def __init__(self, style: str = "APA"):
        self.style = style.upper()

    def build_entry(self, ref_id: str, metadata: dict) -> str:
        authors = ", ".join(metadata.get("authors", []))
        year = metadata.get("year", "n.d.")
        title = metadata.get("title", ref_id)
        source = metadata.get("source", "")

        if self.style == "APA":
            return f"{authors} ({year}). {title}. {source}."

        if self.style == "IEEE":
            index = metadata.get("index")
            return f"[{index}] {authors}, \"{title},\" {source}, {year}."

        if self.style == "MLA":
            return f"{authors}. \"{title}.\" {source}, {year}."

        return f"{authors} ({year}). {title}."
