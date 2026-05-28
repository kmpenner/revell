
import os
import json
import re

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
BIB_PATH = os.path.join(ROOT_DIR, "metadata", "bibliography.json")

# Stop words to ignore when picking "significant" words
STOP_WORDS = {"the", "a", "an", "of", "and", "in", "to", "for", "with", "on", "at", "by", "from", "is", "as", "into"}

def get_significant_words(title, num_words=3):
    # Remove special characters and split
    words = re.findall(r'\b\w+\b', title.lower())
    # Filter stops
    significant = [w.capitalize() for w in words if w not in STOP_WORDS]
    if not significant:
        significant = [w.capitalize() for w in words[:num_words]]
    return " ".join(significant[:num_words])

def main():
    if not os.path.exists(BIB_PATH):
        print("Bibliography not found.")
        return

    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        bibliography = json.load(f)

    if not os.path.exists(ARTICLES_DIR):
        print("Articles directory not found.")
        return

    folders = [f for f in os.listdir(ARTICLES_DIR) if os.path.isdir(os.path.join(ARTICLES_DIR, f))]

    count = 0
    for folder in folders:
        # Extract ID (e.g. 07a.01)
        match = re.search(r'(\d{2}a\.\d{2})', folder)
        if not match:
            continue

        full_id = match.group(1)
        # Convert to bib format (7.a.01)
        parts = full_id.split('.')
        bib_id = f"{int(parts[0][1])}.a.{parts[1]}"

        title = bibliography.get(bib_id)
        if not title:
            # Try fallback to just 7.a.XX if needed, or skip
            continue

        short_title = get_significant_words(title)
        new_name = f"{full_id} - {short_title}"

        old_path = os.path.join(ARTICLES_DIR, folder)
        new_path = os.path.join(ARTICLES_DIR, new_name)

        if old_path != new_path:
            print(f"Renaming folder: {folder} -> {new_name}")
            try:
                os.rename(old_path, new_path)
                count += 1
            except Exception as e:
                print(f"  Error: {e}")

    print(f"\nRenamed {count} folders.")

if __name__ == "__main__":
    main()
