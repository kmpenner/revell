
import os
import shutil
import re

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")

def main():
    if not os.path.exists(ARTICLES_DIR):
        print("Articles directory not found.")
        return

    # Files in the root of Articles
    files = [f for f in os.listdir(ARTICLES_DIR) if os.path.isfile(os.path.join(ARTICLES_DIR, f))]

    for filename in files:
        if not filename.lower().endswith(".pdf"):
            continue

        # Extract ID (e.g., "07a.03")
        match = re.search(r"(\d{2}a\.\d{2})", filename)
        if match:
            article_id = match.group(1)

            # Find target folder
            target_folder = None
            for folder in os.listdir(ARTICLES_DIR):
                if folder.startswith(article_id) and os.path.isdir(os.path.join(ARTICLES_DIR, folder)):
                    target_folder = folder
                    break

            if target_folder:
                dest_dir = os.path.join(ARTICLES_DIR, target_folder)
                src_path = os.path.join(ARTICLES_DIR, filename)
                dest_path = os.path.join(dest_dir, filename)

                print(f"Moving {filename} -> {target_folder}")
                shutil.move(src_path, dest_path)
            else:
                print(f"No folder found for {article_id} (file: {filename})")
        else:
            print(f"No ID found in filename: {filename}")

if __name__ == "__main__":
    main()
