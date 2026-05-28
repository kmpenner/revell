
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

        # Extract article ID (e.g., "07a.01")
        match = re.search(r"(\d{2}a\.\d{2})", folder_name)
        if match:
            article_id = match.group(1)
        else:
            continue

        files = os.listdir(folder_path)

        # Sort files to handle multiple parts consistently if they exist
        pdfs = sorted([f for f in files if f.lower().endswith(".pdf")])
        mds = sorted([f for f in files if f.lower().endswith(".md") and not f.lower().startswith("transcription")])
        xmls = [f for f in files if f.lower().endswith(".xml") and "transcription" in f.lower()]

        # Rename PDFs
        for i, pdf in enumerate(pdfs):
            ext = ".pdf"
            if len(pdfs) == 1:
                new_name = f"{article_id}{ext}"
            else:
                new_name = f"{article_id}_p{i+1}{ext}"

            old_path = os.path.join(folder_path, pdf)
            new_path = os.path.join(folder_path, new_name)
            if old_path != new_path:
                print(f"Renaming {pdf} -> {new_name}")
                if os.path.exists(new_path):
                    # Intermediate rename to avoid collision
                    temp_path = new_path + ".tmp"
                    os.rename(old_path, temp_path)
                    os.rename(temp_path, new_path)
                else:
                    os.rename(old_path, new_path)
                count += 1

        # Rename MDs (metadata files)
        for i, md in enumerate(mds):
            ext = ".md"
            if len(mds) == 1:
                new_name = f"{article_id}{ext}"
            else:
                new_name = f"{article_id}_p{i+1}{ext}"

            old_path = os.path.join(folder_path, md)
            new_path = os.path.join(folder_path, new_name)
            if old_path != new_path:
                print(f"Renaming {md} -> {new_name}")
                if os.path.exists(new_path):
                    temp_path = new_path + ".tmp"
                    os.rename(old_path, temp_path)
                    os.rename(temp_path, new_path)
                else:
                    os.rename(old_path, new_path)
                count += 1

        # Handle transcription files
        for xml in xmls:
            # Standardize to transcription_tei.xml
            new_name = "transcription_tei.xml"
            old_path = os.path.join(folder_path, xml)
            new_path = os.path.join(folder_path, new_name)
            if old_path != new_path:
                print(f"Renaming {xml} -> {new_name}")
                if os.path.exists(new_path):
                    os.remove(old_path) # If we have multiple, the newest tei one should win? Or just keep it.
                else:
                    os.rename(old_path, new_path)
                count += 1

    print(f"\nFinal Cleanup: Renamed {count} files.")

if __name__ == "__main__":
    main()
