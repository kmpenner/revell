
import os
import json
import fitz  # PyMuPDF
import re
import shutil
from difflib import SequenceMatcher

OCR_DIR = r"g:\My Drive\Research\Revell\OCR"
ARTICLES_DIR = r"g:\My Drive\Research\Revell\07a Articles"
BOOKS_DIR = r"g:\My Drive\Research\Revell\07b Books"
BIB_PATH = r"g:\My Drive\Research\Revell\metadata\bibliography.json"

def load_bibliography():
    """Load the bibliography JSON."""
    if not os.path.exists(BIB_PATH):
        print(f"Bibliography not found at {BIB_PATH}")
        return {}
    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_target_folder(article_id):
    """Find the existing folder for a given article ID (e.g., '7.a.30' or '7.b.01')."""
    if article_id.startswith("7.a."):
        prefix = article_id.replace("7.a.", "07a.")
        base_dir = ARTICLES_DIR
    elif article_id.startswith("7.b."):
        prefix = article_id.replace("7.b.", "07b.")
        # Handle 7.b.1 (one digit) vs 7.b.01 (two digits)
        # CV uses 7.b.01, but folders might use 07b.1
        match = re.search(r'7\.b\.(\d+)', article_id)
        if match:
            num = int(match.group(1))
            prefix = f"07b.{num}" # 07b.1
        base_dir = BOOKS_DIR
    else:
        return None

    if not os.path.exists(base_dir):
        return None

    for folder in os.listdir(base_dir):
        if folder.startswith(prefix):
            return os.path.join(base_dir, folder)
    return None

def normalize_text(text):
    """Normalize text for better matching."""
    return re.sub(r'\s+', ' ', text).lower().strip()

def extract_text_as_markdown(pdf_path):
    """Extract text from PDF and format as basic Markdown."""
    doc = fitz.open(pdf_path)
    md_content = ""
    for page in doc:
        text = page.get_text()
        md_content += text + "\n\n---\n\n"  # Page break marker
    doc.close()
    return md_content

def classify_pdf(pdf_path, bib_data):
    """Determine the article ID based on PDF content."""
    # Extract first few pages for matching
    doc = fitz.open(pdf_path)
    # Check first 3 pages or fewer
    sample_text = ""
    for i in range(min(3, len(doc))):
        sample_text += doc[i].get_text()
    doc.close()

    normalized_sample = normalize_text(sample_text)

    best_match_id = None
    highest_ratio = 0.0

    for art_id, citation in bib_data.items():
        # Title is usually the first part of citation in quotes
        match = re.search(r'"([^"]+)"', citation)
        if match:
            title = match.group(1)
            normalized_title = normalize_text(title)

            # Simple substring check first
            if normalized_title in normalized_sample:
                # Strong match if title is fully present
                return art_id

            # Fuzzy match ratio
            ratio = SequenceMatcher(None, normalized_title, normalized_sample).find_longest_match(0, len(normalized_title), 0, len(normalized_sample)).size / len(normalized_title)
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match_id = art_id

    # Threshold for fuzzy match (e.g., 60% of title found contiguously or similar)
    if highest_ratio > 0.6:
        return best_match_id

    return None

def main():
    bib_data = load_bibliography()
    if not bib_data:
        return

    # List all generated/OCR PDFs
    pdf_files = [f for f in os.listdir(OCR_DIR) if f.lower().endswith('.pdf')]

    print(f"Found {len(pdf_files)} PDFs in {OCR_DIR}")

    for filename in pdf_files:
        pdf_path = os.path.join(OCR_DIR, filename)
        print(f"\nProcessing {filename}...")

        # 1. Classify
        article_id = classify_pdf(pdf_path, bib_data)

        if article_id:
            print(f"  Matched to: {article_id} - {bib_data[article_id][:50]}...")

            # 2. Extract full markdown
            md_content = extract_text_as_markdown(pdf_path)

            # 3. Find destination
            target_folder = find_target_folder(article_id)
            if target_folder:
                # Move PDF
                dest_pdf = os.path.join(target_folder, filename)
                if os.path.exists(dest_pdf):
                    print(f"  Destination PDF exists: {dest_pdf}. Skipping move.")
                else:
                    shutil.move(pdf_path, dest_pdf)
                    print(f"  Moved PDF to {target_folder}")

                # Save Markdown
                md_filename = os.path.splitext(filename)[0] + ".md"
                dest_md = os.path.join(target_folder, md_filename)

                # Add frontmatter
                frontmatter = f"---\ntitle: \"{article_id}\"\nfilename: \"{filename}\"\n---\n\n"
                with open(dest_md, 'w', encoding='utf-8') as f:
                    f.write(frontmatter + md_content)
                print(f"  Saved Markdown to {dest_md}")
            else:
                print(f"  Could not find folder for {article_id} (07a format).")
        else:
            print("  No match found in bibliography.")

if __name__ == "__main__":
    main()
