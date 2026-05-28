
import os
import json
import fitz  # PyMuPDF
import base64
from openai import OpenAI
import re
import shutil
from difflib import SequenceMatcher

# Configuration
OCR_DIR = r"g:\My Drive\Research\Revell\OCR"
ARTICLES_DIR = r"g:\My Drive\Research\Revell\07a Articles"
BOOKS_DIR = r"g:\My Drive\Research\Revell\07b Books"
BIB_PATH = r"g:\My Drive\Research\Revell\metadata\bibliography.json"
API_KEY_PATH = r"g:\My Drive\Research\Revell\metadata\openrouter_api_key.txt"

def get_api_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, 'r') as f:
            return f.read().strip()
    return os.environ.get("OPENROUTER_API_KEY")

def load_bibliography():
    if not os.path.exists(BIB_PATH):
        return {}
    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def pdf_page_to_base64(pdf_path, page_num=0):
    doc = fitz.open(pdf_path)
    if page_num >= len(doc):
        return None
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0)) # 2x distinct for OCR
    img_data = pix.tobytes("png")
    doc.close()
    return base64.b64encode(img_data).decode('utf-8')

def identify_article_with_llm(client, base64_image, bib_data):
    """Ask LLM to identify the article from the first page image."""

    # Prepare bibliography list for context (titles only to save tokens)
    titles = [f"{k}: {v}" for k, v in bib_data.items()]
    bib_text = "\n".join(titles)

    prompt = f"""
    You are an expert bibliographer. I will show you the first page of an academic article or book.
    Your task is to identify which item from the provided bibliography this corresponds to.

    Bibliography:
    {bib_text}

    If you find a match, return the ID (e.g., 7.a.30 or 7.b.01).
    If you are unsure but see a clear title, return "TITLE: <extracted title>".
    I am looking for exact matches.
    """

    response = client.chat.completions.create(
        model="qwen/qwen3-vl-235b-a22b-thinking",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content.strip()

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

def main():
    api_key = get_api_key()
    if not api_key:
        print("No API key found.")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    bib_data = load_bibliography()

    # Files to process
    target_files = [f for f in os.listdir(OCR_DIR) if f.lower().endswith('.pdf')]

    for filename in target_files:
        pdf_path = os.path.join(OCR_DIR, filename)
        if not os.path.exists(pdf_path):
            print(f"File not found: {filename}")
            continue

        print(f"\nProcessing {filename}...")

        # Get image of first page
        img_b64 = pdf_page_to_base64(pdf_path, 0)

        # Ask LLM
        result = identify_article_with_llm(client, img_b64, bib_data)
        print(f"LLM Identification: {result}")

        # Extract ID
        match = re.search(r'7\.[ab]\.\d+', result)
        if match:
            article_id = match.group(0)
            print(f"Identified ID: {article_id}")

            target_folder = find_target_folder(article_id)
            if target_folder:
                dest_pdf = os.path.join(target_folder, filename)

                # Check for duplicate content (size check)
                existing_pdfs = [f for f in os.listdir(target_folder) if f.lower().endswith('.pdf')]
                is_duplicate = False
                source_size = os.path.getsize(pdf_path)

                for existing in existing_pdfs:
                    existing_path = os.path.join(target_folder, existing)
                    if os.path.getsize(existing_path) == source_size:
                        print(f"  Duplicate of existing file {existing}. Moving to superfluous/duplicates.")
                        superfluous_dir = os.path.join(r"g:\My Drive\Research\Revell\superfluous", "duplicates")
                        if not os.path.exists(superfluous_dir):
                            os.makedirs(superfluous_dir)
                        shutil.move(pdf_path, os.path.join(superfluous_dir, filename))
                        is_duplicate = True
                        break

                if not is_duplicate:
                    shutil.move(pdf_path, dest_pdf)
                    print(f"  Moved to {target_folder}")

                    # Create a simple markdown stub
                    md_filename = os.path.splitext(filename)[0] + ".md"
                    with open(os.path.join(target_folder, md_filename), 'w', encoding='utf-8') as f:
                        f.write(f"---\ntitle: \"{article_id}\"\nfilename: \"{filename}\"\n---\n\nIdentified as {article_id} by LLM visual inspection.\n")
            else:
                print(f"  Folder not found for {article_id}")
        else:
            print("  Could not identify article ID from response.")

if __name__ == "__main__":
    main()
