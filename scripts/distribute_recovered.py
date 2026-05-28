
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell"
RECOVERED_DIR = os.path.join(ROOT_DIR, "recovered")
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")

def main():
    if not os.path.exists(RECOVERED_DIR):
        print("Recovered directory not found.")
        return

    files = os.listdir(RECOVERED_DIR)
    for filename in files:
        if not filename.lower().endswith(".pdf"):
            continue

        # Extract ID (e.g., "07a.32")
        # Format is usually "07a.XX_Title.pdf"
        article_id = filename.split("_")[0]

        # Find target folder in 07a Articles
        target_folder = None
        for folder in os.listdir(ARTICLES_DIR):
            if folder.startswith(article_id) and os.path.isdir(os.path.join(ARTICLES_DIR, folder)):
                target_folder = folder
                break

        if target_folder:
            dest_folder_path = os.path.join(ARTICLES_DIR, target_folder)

            # Check for existing files to determine part number if necessary
            existing_pdfs = [f for f in os.listdir(dest_folder_path) if f.lower().endswith(".pdf")]

            if not existing_pdfs:
                new_filename = f"{article_id}.pdf"
            else:
                # If there are already PDFs, we might be adding a part or version
                # But the user said "there should not be any articles in multiple parts"
                # implying they should ideally be one file or distinct.
                # However, if we have two different files for 07a.36, let's keep them distinct for now.
                new_filename = f"{article_id}_v{len(existing_pdfs) + 1}.pdf"

            src_path = os.path.join(RECOVERED_DIR, filename)
            dest_path = os.path.join(dest_folder_path, new_filename)

            print(f"Moving {filename} -> {target_folder}/{new_filename}")
            shutil.move(src_path, dest_path)
        else:
            print(f"Could not find target folder for {article_id} (file: {filename})")

if __name__ == "__main__":
    main()
