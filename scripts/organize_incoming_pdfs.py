
import os
import shutil
import sys
from markitdown import MarkItDown

# Ensure output is UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
OCR_DIR = os.path.join(ROOT_DIR, "OCR")

def get_article_folders():
    folders = []
    if not os.path.exists(ARTICLES_DIR):
        print(f"Error: {ARTICLES_DIR} does not exist.")
        return folders

    for item in os.listdir(ARTICLES_DIR):
        if item.startswith("07a.") and os.path.isdir(os.path.join(ARTICLES_DIR, item)):
            # Extract the title part after " - "
            if " - " in item:
                title = item.split(" - ", 1)[1]
            else:
                title = item
            folders.append({
                'name': item,
                'path': os.path.join(ARTICLES_DIR, item),
                'title': title.lower()
            })
    return folders

def main():
    markitdown = MarkItDown()
    article_folders = get_article_folders()

    if not article_folders:
        print("No article folders found.")
        return

    if not os.path.exists(OCR_DIR):
        print(f"OCR Directory not found: {OCR_DIR}")
        return

    pdfs = [f for f in os.listdir(OCR_DIR) if f.lower().endswith(".pdf")]

    if not pdfs:
        print("No PDFs found in OCR directory.")
        return

    print(f"Found {len(pdfs)} PDFs to process.")

    for pdf_name in pdfs:
        pdf_path = os.path.join(OCR_DIR, pdf_name)
        print(f"Processing {pdf_name}...")

        try:
            result = markitdown.convert(pdf_path)
            text = result.text_content.lower()

            # Identify which folder matches
            matched_folder = None
            max_match_score = 0

            for folder in article_folders:
                # Try exact title match first (case-insensitive)
                if folder['title'] in text:
                    matched_folder = folder
                    break

                # Check if the folder name (e.g. 07a.01) is in the filename or text?
                folder_id = folder['name'].split(" - ")[0].split(".")[1] # e.g. "01"
                if f"07a.{folder_id}" in text or f"article {folder_id}" in text:
                     matched_folder = folder
                     break

                # Fallback: look for unique keywords
                words = [w for w in folder['title'].replace(',', '').replace(';', '').replace('(', '').replace(')', '').split() if len(w) > 4]
                if words:
                    match_count = sum(1 for w in words if w in text)
                    if match_count > len(words) * 0.7: # 70% of long words match
                        if match_count > max_match_score:
                            max_match_score = match_count
                            matched_folder = folder

            if matched_folder:
                print(f"  Matched: {matched_folder['name']}")
                target_path = os.path.join(matched_folder['path'], pdf_name)

                # Handle overwrite/duplicates
                if os.path.exists(target_path):
                     print(f"  File exists at target, appending timestamp.")
                     base, ext = os.path.splitext(pdf_name)
                     import time
                     timestamp = int(time.time())
                     target_path = os.path.join(matched_folder['path'], f"{base}_{timestamp}{ext}")

                print(f"  Moving to: {target_path}")
                shutil.move(pdf_path, target_path)
                print(f"  Moved successfully.")
            else:
                print(f"  No match found for {pdf_name}")
                snippet = text[:500].replace('\n', ' ')
                print(f"  Snippet: {snippet}")

        except Exception as e:
            print(f"  Error processing {pdf_name}: {e}")

if __name__ == "__main__":
    main()
