
import os
import io
import json
import fitz
import base64
from openai import OpenAI
import logging
import time
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
BIB_PATH = os.path.join(ROOT_DIR, "metadata", "bibliography.json")
RECOVERED_DIR = os.path.join(ROOT_DIR, "recovered")

def get_as_base64(pix):
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

def identify_page(client, pix, bibliography, model="google/gemma-3-4b-it"):
    img_b64 = get_as_base64(pix)

    prompt = f"""
    Is this the first page of a scholarly article?
    If yes, identify the title and match it to this list of Article IDs:
    {json.dumps(bibliography, indent=2)}

    Return a JSON object:
    {{
      "is_first_page": boolean,
      "article_id": "7.a.XX" or null,
      "title": "string" or null
    }}
    Output ONLY the JSON.
    """

    try:
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
        content = response.choices[0].message.content.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        logging.error(f"Error identifying page: {e}")
        return None

def main():
    os.makedirs(RECOVERED_DIR, exist_ok=True)

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

    # Folders to check for merged files
    check_folders = [
        "07a.01 - The Order of the Elements in the Verbal Statement Clause in 1Q Serek",
        "07a.03 - Sign and Sound in the Study of Written Texts",
        "07a.08 - The Oldest Accent List in the Diqduqe ha-Te'amim",
        "07a.10 - A New Sybsystem of Tibero-Palestinian Vocalization",
        "07a.19 - Pausal Forms in Biblical Hebrew their function, origin, and significance",
        "07a.24 - The Battle with Benjamin (Jud. XX 29-48) and Hebrew Narrative Techniques",
        "07a.30 - The Conditioning of Stress Position in Waw Consecutive Perfect Forms in Biblical Hebrew",
        "07a.32 - First Person Imperfect Forms with Waw Consecutive",
        "07a.41 - Language and Interpretation in 1 Kings 20",
        "07a.44 - Concord with Collectives in Biblical Narrative",
        "07a.49 - The Interpretative Significance of the Masoretic Punctuation"
    ]

    for folder_name in check_folders:
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if not os.path.exists(folder_path):
            continue

        pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf") and "_part" not in f] # Avoid already split files
        if not pdfs:
            continue

        print(f"\nScanning folder: {folder_name}...")

        for pdf_file in pdfs:
            pdf_path = os.path.join(folder_path, pdf_file)
            try:
                doc = fitz.open(pdf_path)
            except Exception as e:
                print(f"  Error opening {pdf_file}: {e}")
                continue

            articles_found = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))

                result = identify_page(client, pix, bibliography)
                if result and result.get("is_first_page") and result.get("article_id"):
                    articles_found.append((page_num, result["article_id"], result["title"]))
                    print(f"  Page {page_num}: Found {result['article_id']} - {result['title']}")

            if len(articles_found) > 1:
                print(f"  Detected {len(articles_found)} articles in {pdf_file}. Exploding...")

                for i in range(len(articles_found)):
                    start_page, article_id, title = articles_found[i]
                    end_page = articles_found[i+1][0] if i+1 < len(articles_found) else len(doc)

                    # Create new PDF
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page-1)

                    sanitized_title = "".join(c for c in title if c.isalnum() or c in (' ', '.', '-', '_')).strip().replace(' ', '_')
                    folder_id = article_id.replace('7.a.', '07a.').replace('7.b.', '07b.')
                    new_name = f"{folder_id}_{sanitized_title}.pdf"
                    if len(new_name) > 100: new_name = new_name[:100] + ".pdf"

                    output_path = os.path.join(RECOVERED_DIR, new_name)
                    new_doc.save(output_path)
                    print(f"    Saved {new_name} to recovered/")
                    new_doc.close()

                doc.close()
                # Move original to backup
                backup_dir = os.path.join(ROOT_DIR, "backups")
                os.makedirs(backup_dir, exist_ok=True)
                time.sleep(1)
                try:
                    shutil.move(pdf_path, os.path.join(backup_dir, pdf_file))
                except:
                    print(f"  Warning: Could not move {pdf_file} to backup. Please close it manually.")
            else:
                doc.close()
                print(f"  Only 1 article found in {pdf_file}. No action needed.")

if __name__ == "__main__":
    main()
