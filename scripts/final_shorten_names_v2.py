
import os
import re

ARTICLES_DIR = r"g:\My Drive\Research\Revell\07a Articles"

def main():
    if not os.path.exists(ARTICLES_DIR):
        print("Articles directory not found.")
        return

    count = 0
    for folder_name in os.listdir(ARTICLES_DIR):
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        match = re.search(r"(\d{2}a\.\d{2})", folder_name)
        if match:
            article_id = match.group(1)
        else:
            continue

        # Get all files and categorize
        files = os.listdir(folder_path)
        pdfs = sorted([f for f in files if f.lower().endswith(".pdf")])
        mds = sorted([f for f in files if f.lower().endswith(".md") and not f.lower().startswith("transcription")])
        xmls = [f for f in files if f.lower().endswith(".xml") and "transcription" in f.lower()]

        # Robust rename function
        def safe_rename(old_name, new_base, ext):
            nonlocal count
            if old_name.lower() == (new_base + ext).lower():
                return

            new_name = new_base + ext
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)

            if os.path.exists(new_path):
                # If they are different files, use a suffix
                if old_name.lower() != new_name.lower():
                    # Try suffixes until one works
                    i = 1
                    while os.path.exists(os.path.join(folder_path, f"{new_base}_v{i}{ext}")):
                        i += 1
                    new_name = f"{new_base}_v{i}{ext}"
                    new_path = os.path.join(folder_path, new_name)
                    print(f"Collision! Renaming {old_name} -> {new_name}")
                    os.rename(old_path, new_path)
                    count += 1
            else:
                print(f"Renaming {old_name} -> {new_name}")
                os.rename(old_path, new_path)
                count += 1

        # Rename PDFs
        for i, pdf in enumerate(pdfs):
            if len(pdfs) == 1:
                safe_rename(pdf, article_id, ".pdf")
            else:
                safe_rename(pdf, f"{article_id}_p{i+1}", ".pdf")

        # Rename MDs
        for i, md in enumerate(mds):
            if len(mds) == 1:
                safe_rename(md, article_id, ".md")
            else:
                safe_rename(md, f"{article_id}_p{i+1}", ".md")

        # Handle transcription files
        for xml in xmls:
            if xml != "transcription_tei.xml":
                old_path = os.path.join(folder_path, xml)
                new_path = os.path.join(folder_path, "transcription_tei.xml")
                if os.path.exists(new_path):
                    # If we have multiple, let's keep them distinct?
                    # Only if they are genuinely different.
                    # For now, let's just use v numbering.
                    safe_rename(xml, "transcription_tei", ".xml")
                else:
                    print(f"Renaming {xml} -> transcription_tei.xml")
                    os.rename(old_path, new_path)
                    count += 1

    print(f"\nFinal Cleanup: Renamed {count} files.")

if __name__ == "__main__":
    main()
