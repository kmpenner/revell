
import os
import shutil
from markitdown import MarkItDown

ROOT_DIR = r"g:\My Drive\Research\Revell"
OCR_DIR = os.path.join(ROOT_DIR, "OCR")

def get_article_folders():
    folders = []
    for item in os.listdir(ROOT_DIR):
        if item.startswith("07a.") and os.path.isdir(os.path.join(ROOT_DIR, item)):
            # Extract the title part after " - "
            if " - " in item:
                title = item.split(" - ", 1)[1]
            else:
                title = item
            folders.append({
                'name': item,
                'path': os.path.join(ROOT_DIR, item),
                'title': title.lower()
            })
    return folders

def main():
    markitdown = MarkItDown()
    article_folders = get_article_folders()

    pdfs = [f for f in os.listdir(OCR_DIR) if f.endswith(".pdf")]

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
                # Check if the title is in the text
                # We can use a simple substring check or look for key words
                # Some titles might be slightly different in OCR

                # Try exact title match first
                if folder['title'] in text:
                    matched_folder = folder
                    break

                # Fallback: look for unique keywords if title is long
                # This is just a heuristic
                words = [w for w in folder['title'].replace(',', '').replace(';', '').split() if len(w) > 4]
                if words:
                    match_count = sum(1 for w in words if w in text)
                    if match_count > len(words) * 0.7: # 70% of long words match
                        if match_count > max_match_score:
                            max_match_score = match_count
                            matched_folder = folder

            if matched_folder:
                print(f"  Matched: {matched_folder['name']}")
                target_path = os.path.join(matched_folder['path'], pdf_name)
                shutil.move(pdf_path, target_path)
                print(f"  Moved to {matched_folder['name']}")
            else:
                print(f"  No match found for {pdf_name}")
                # Print a snippet of the text to help manual identification if needed
                print(f"  Text snippet: {text[:500].replace('\\n', ' ')}")

        except Exception as e:
            print(f"  Error processing {pdf_name}: {e}")

if __name__ == "__main__":
    main()
