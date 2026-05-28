
import os
import io
import json
import fitz
import base64
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_DIR = r"g:\My Drive\Research\Revell"
SCANS_DIR = os.path.join(ROOT_DIR, "scans")
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
BIB_PATH = os.path.join(ROOT_DIR, "metadata", "bibliography.json")

def get_as_base64(pix):
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

def identify_pdf(client, pdf_path, bibliography, model="google/gemma-3-4b-it"):
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        img_b64 = get_as_base64(pix)
        doc.close()
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return None

    prompt = f"""
    Identify the title of this scholarly article from its first page.
    Match it to this bibliography list:
    {json.dumps(bibliography, indent=2)}

    Return a JSON object:
    {{
      "article_id": "7.a.XX" or null,
      "title": "Detected Title",
      "confidence": "high/medium/low"
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
        logging.error(f"Error identifying PDF: {e}")
        return None

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        with open(os.path.join(ROOT_DIR, "metadata", "openrouter_api_key.txt"), 'r') as f:
            api_key = f.read().strip()

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        bibliography = json.load(f)

    if not os.path.exists(SCANS_DIR):
        print("Scans directory not found.")
        return

    for pdf_file in os.listdir(SCANS_DIR):
        if not pdf_file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(SCANS_DIR, pdf_file)
        print(f"Analyzing {pdf_file}...")

        result = identify_pdf(client, pdf_path, bibliography)

        if result and result.get('article_id'):
            article_id = result['article_id']
            print(f"  MATCH: {article_id} - {result['title']}")

            # Map "7.a.XX" to "07a.XX"
            parts = article_id.split(".")
            folder_id = f"0{parts[0]}{parts[1]}.{parts[2]}"

            target_folder = None
            for f in os.listdir(ARTICLES_DIR):
                if f.startswith(folder_id):
                    target_folder = f
                    break

            if target_folder:
                dest_dir = os.path.join(ARTICLES_DIR, target_folder)

                # Create sanitized name
                title = result['title']
                sanitized_title = "".join(c for c in title if c.isalnum() or c in (' ', '.', '-', '_')).strip().replace(' ', '_')
                new_name = f"{folder_id}_{sanitized_title}.pdf"
                if len(new_name) > 100: new_name = new_name[:100] + ".pdf"

                dest_path = os.path.join(dest_dir, new_name)

                print(f"  -> Moving to {target_folder}/{new_name}")
                import shutil
                shutil.copy(pdf_path, dest_path) # Copy first to be safe
            else:
                print(f"  Target folder {folder_id} not found.")
        else:
            print(f"  No match found for {pdf_file}")

if __name__ == "__main__":
    main()
