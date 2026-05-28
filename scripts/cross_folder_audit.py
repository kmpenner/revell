
import os
import io
import json
import fitz
import base64
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
BIB_PATH = os.path.join(ROOT_DIR, "metadata", "bibliography.json")
BACKUPS_DIR = os.path.join(ROOT_DIR, "backups")
MISFILED_DIR = os.path.join(ROOT_DIR, "misfiled")

def get_as_base64(pix):
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

def identify_content(client, pdf_path, bibliography, empty_ids, model="google/gemma-3-4b-it"):
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
        img_b64 = get_as_base64(pix)
        doc.close()
    except Exception as e:
        return None

    prompt = f"""
    Identify the title and article ID of the scholarly article on this page.
    Candidate IDs you are looking for specifically: {json.dumps(empty_ids)}

    Full Bibliography for reference:
    {json.dumps(bibliography, indent=2)}

    Return a JSON object:
    {{
      "article_id": "7.a.XX",
      "title": "Detected Title",
      "confidence": "high/medium/low",
      "is_match_for_empty": true/false
    }}
    Output ONLY THE JSON.
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
        logging.error(f"API Error identifying PDF: {e}")
        return None

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        with open(os.path.join(ROOT_DIR, "metadata", "openrouter_api_key.txt"), 'r') as f:
            api_key = f.read().strip()

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        bibliography = json.load(f)

    # Folders with 0 PDFs
    empty_folders = []
    folders = sorted([f for f in os.listdir(ARTICLES_DIR) if os.path.isdir(os.path.join(ARTICLES_DIR, f))])
    for f in folders:
        pdfs = [p for p in os.listdir(os.path.join(ARTICLES_DIR, f)) if p.lower().endswith(".pdf")]
        if not pdfs:
            empty_folders.append(f)

    empty_ids = []
    for f in empty_folders:
        match = re.search(r'(\d+[a-z]?)\.(\d+)', f)
        if match:
            sec, num = match.groups()
            sec_fmt = ".".join(list(sec.lstrip('0'))) if sec.startswith('0') else sec
            empty_ids.append(f"{sec_fmt}.{num}")

    print(f"Empty IDs: {empty_ids}")

    # Folders with >1 PDF
    bloated_folders = []
    for f in folders:
        pdfs = [p for p in os.listdir(os.path.join(ARTICLES_DIR, f)) if p.lower().endswith(".pdf")]
        if len(pdfs) > 1:
            bloated_folders.append(f)

    results = []

    # Audit bloated folders
    for folder in bloated_folders:
        folder_path = os.path.join(ARTICLES_DIR, folder)
        pdfs = [p for p in os.listdir(folder_path) if p.lower().endswith(".pdf")]
        print(f"\nAuditing bloated folder: {folder}")
        for pdf in pdfs:
            pdf_path = os.path.join(folder_path, pdf)
            res = identify_content(client, pdf_path, bibliography, empty_ids)
            if res:
                res['source_folder'] = folder
                res['filename'] = pdf
                print(f"  {pdf}: Identified as {res.get('article_id')} ({res.get('title')}) - Match Empty: {res.get('is_match_for_empty')}")
                results.append(res)

    # Audit misfiled & backup just in case
    for dir_path in [MISFILED_DIR, BACKUPS_DIR]:
        if os.path.exists(dir_path):
            print(f"\nAuditing {os.path.basename(dir_path)} folder...")
            pdfs = [p for p in os.listdir(dir_path) if p.lower().endswith(".pdf")]
            for pdf in pdfs:
                pdf_path = os.path.join(dir_path, pdf)
                res = identify_content(client, pdf_path, bibliography, empty_ids)
                if res:
                    res['source_folder'] = os.path.basename(dir_path)
                    res['filename'] = pdf
                    print(f"  {pdf}: Identified as {res.get('article_id')} - Match Empty: {res.get('is_match_for_empty')}")
                    results.append(res)

    with open(os.path.join(ROOT_DIR, "cross_folder_audit_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Propose moves
    print("\n--- PROPOSED MOVES ---")
    for r in results:
        if r.get('is_match_for_empty') or r.get('article_id') in empty_ids:
            target_id = r.get('article_id')
            # Find target folder name
            target_folder = None
            # Need to match 7.a.11 to 07a.11
            parts = target_id.split('.')
            search_prefix = f"0{parts[0]}{parts[1]}.{parts[2]}" if len(parts) == 3 else f"0{parts[0]}.{parts[1]}"
            for f in folders:
                if f.startswith(search_prefix):
                    target_folder = f
                    break

            if target_folder:
                 print(f"MOVE: {r['source_folder']}/{r['filename']} -> {target_folder}")
            else:
                 print(f"MOVE: {r['source_folder']}/{r['filename']} -> (Target folder for {target_id} not found!)")

if __name__ == "__main__":
    import re
    main()
