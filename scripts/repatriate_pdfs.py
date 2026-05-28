
import os
import io
import base64
import json
import re
import fitz
from openai import OpenAI
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
BIB_PATH = os.path.join(ROOT_DIR, "metadata", "bibliography.json")

def get_as_base64(pix):
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

def identify_article(client, pdf_path, bibliography, model="google/gemini-3-flash-preview"):
    """Use vision model to identify an article from its first page."""
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # 2x zoom for clarity
        img_b64 = get_as_base64(pix)
        doc.close()

        prompt = f"""
        Below is the first page of a scholarly article.
        Please identify the Title and Author from the image.

        Author is expected to be E. J. Revell.

        Compare the identified title to this bibliographic list:
        {json.dumps(bibliography, indent=2)}

        Return a JSON object with:
        - "detected_title": string
        - "matched_id": the ID from the bibliography (e.g., "7.a.01")
        - "confidence": 0-1

        If no match is found, set matched_id to null.
        Output ONLY the JSON.
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                    ]
                }
            ]
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()

        return json.loads(content)
    except Exception as e:
        logging.error(f"Error identifying {pdf_path}: {e}")
        return None

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key_path = os.path.join(ROOT_DIR, "metadata", "openrouter_api_key.txt")
        if os.path.exists(api_key_path):
            with open(api_key_path, 'r') as f:
                api_key = f.read().strip()

    if not api_key:
        print("API Key not found.")
        return

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        bibliography = json.load(f)

    # Folders to audit (multi-part folders)
    audit_folders = [
        "07a.19 - Pausal Forms in Biblical Hebrew their function, origin, and significance",
        "07a.30 - The Conditioning of Stress Position in Waw Consecutive Perfect Forms in Biblical Hebrew",
        "07a.49 - The Interpretative Significance of the Masoretic Punctuation",
        "07a.41 - Language and Interpretation in 1 Kings 20",
        "07a.10 - A New Sybsystem of Tibero-Palestinian Vocalization"
    ]

    for folder_name in audit_folders:
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if not os.path.exists(folder_path):
            continue

        print(f"\n--- Auditing Folder: {folder_name} ---")
        pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

        for pdf in pdfs:
            pdf_path = os.path.join(folder_path, pdf)
            print(f"Checking {pdf}...")

            result = identify_article(client, pdf_path, bibliography)
            if result and result.get('matched_id'):
                matched_id = result['matched_id']
                # Correct folder name part (e.g. "07a.24")
                # bibliography key is "7.a.24", we want folder starting with "07a.24"
                parts = matched_id.split('.')
                # matched_id "7.a.24" -> "07a.24"
                folder_id = f"0{parts[0]}{parts[1]}.{parts[2]}"

                # Check if it's already in the right folder (by ID)
                if folder_name.startswith(folder_id):
                    print(f"  [OK] Correctly placed: {matched_id}")
                else:
                    print(f"  [MISMATCH] Should be {matched_id}! (Detected: {result.get('detected_title')})")
                    # Find target folder
                    target_folder = None
                    for f in os.listdir(ARTICLES_DIR):
                        if f.startswith(folder_id):
                            target_folder = f
                            break

                    if target_folder:
                        target_dir = os.path.join(ARTICLES_DIR, target_folder)
                        print(f"  -> Moving to {target_folder}")
                        # Move PDF
                        shutil.move(pdf_path, os.path.join(target_dir, pdf))
                        # Move MD if it exists
                        md_path = os.path.splitext(pdf_path)[0] + ".md"
                        if os.path.exists(md_path):
                            shutil.move(md_path, os.path.join(target_dir, os.path.basename(md_path)))
                    else:
                        print(f"  [ERROR] Target folder {folder_id} not found!")
            else:
                print(f"  [UNKNOWN] Could not identify article.")

if __name__ == "__main__":
    main()
