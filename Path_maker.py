import os

BASE_DIR = os.getcwd()

FILES_TO_CREATE = [
    # UI
    "ui/app.py",

    # Backend
    "backend/pipeline.py",
    "backend/docx_handler.py",
    "backend/pdf_extractor.py",
    "backend/text_chunker.py",
    "backend/embedder.py",
    "backend/matcher.py",
    "backend/citation_engine.py",
    "backend/bibliography_builder.py",
    "backend/quality_controls.py",

    # Prompts
    "prompts/citation_prompt.txt",

    # Root files
    "config.py",
    "requirements.txt",
    "README.md",
]

def create_files():
    created = []
    skipped = []

    for relative_path in FILES_TO_CREATE:
        full_path = os.path.join(BASE_DIR, relative_path)
        directory = os.path.dirname(full_path)

        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write("")  # empty file
            created.append(relative_path)
        else:
            skipped.append(relative_path)

    print("\n✅ FILE CREATION SUMMARY")
    print("-" * 30)

    if created:
        print("🆕 Created files:")
        for f in created:
            print("  ✔", f)
    else:
        print("🆕 No new files created")

    if skipped:
        print("\n⏭ Skipped (already exist):")
        for f in skipped:
            print("  •", f)

    print("\n🎉 Project is ready for coding!")

if __name__ == "__main__":
    create_files()
