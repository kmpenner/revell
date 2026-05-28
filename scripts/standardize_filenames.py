
import os
import re

ARTICLES_DIR = r"g:\My Drive\Research\Revell\07a Articles"

def sanitize(name):
    # Remove characters that are problematic in filenames but keep spaces/dots/dashes
    return re.sub(r'[\\/*?:"<>|]', '', name).strip().replace(' ', '_')

def main():
    if not os.path.exists(ARTICLES_DIR):
        print("Articles directory not found.")
        return

    for folder_name in os.listdir(ARTICLES_DIR):
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Determine the base name from the folder name
        # Folder is like "07a.01 - Title"
        # We want "07a.01_Title"
        if " - " in folder_name:
            parts = folder_name.split(" - ", 1)
            base_name = f"{parts[0]}_{sanitize(parts[1])}"
        else:
            base_name = sanitize(folder_name)

        # Limit length
        if len(base_name) > 120:
            base_name = base_name[:120]

        files = os.listdir(folder_path)
        pdfs = sorted([f for f in files if f.lower().endswith(".pdf")])
        mds = sorted([f for f in files if f.lower().endswith(".md")])

        # Rename PDFs
        for i, pdf in enumerate(pdfs):
            suffix = f"_part{i+1}" if len(pdfs) > 1 else ""
            new_name = f"{base_name}{suffix}.pdf"
            old_path = os.path.join(folder_path, pdf)
            new_path = os.path.join(folder_path, new_name)

            if old_path.lower() != new_path.lower():
                print(f"Renaming PDF in {folder_name}: {pdf} -> {new_name}")
                try:
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"  Error: {e}")

        # Rename MDs to match
        for i, md in enumerate(mds):
            # If multiple MDs, we might have a problem matching them to PDFs.
            # But usually we have one MD per PDF or one MD for the whole folder.
            # Let's just rename them consistently.
            suffix = f"_part{i+1}" if len(mds) > 1 else ""
            new_name = f"{base_name}{suffix}.md"
            old_path = os.path.join(folder_path, md)
            new_path = os.path.join(folder_path, new_name)

            if old_path.lower() != new_path.lower():
                 # Check if the new name already exists (could happen if we are swapping)
                 if os.path.exists(new_path) and old_path.lower() != new_path.lower():
                     print(f"  Warning: {new_name} already exists. Skipping MD rename.")
                     continue
                 print(f"Renaming MD in {folder_name}: {md} -> {new_name}")
                 try:
                     os.rename(old_path, new_path)
                 except Exception as e:
                     print(f"  Error: {e}")

if __name__ == "__main__":
    main()
