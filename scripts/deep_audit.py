
import os
import io
import base64
import json
import fitz
from openai import OpenAI

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
BIB_PATH = os.path.join(ROOT_DIR, "metadata", "bibliography.json")

def get_as_base64(pix):
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

def identify_article(client, pdf_path, bibliography):
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_b64 = get_as_base64(pix)
        doc.close()

        prompt = f"""
        Identify the title of this scholarly article. Matches it against the list below.
        Author: E. J. Revell.

        List:
        {json.dumps(bibliography, indent=2)}

        Return JSON: {{"id": "7.a.XX", "title": "Detected Title"}}
        If no match, id=null.
        """

        response = client.chat.completions.create(
            model="google/gemini-3-flash-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                ]
            }]
        )
        content = response.choices[0].message.content.strip().replace("```json", "").replace("```", "")
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        with open(os.path.join(ROOT_DIR, "metadata", "openrouter_api_key.txt"), 'r') as f:
            api_key = f.read().strip()

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        bib = json.load(f)

    for item in sorted(os.listdir(ARTICLES_DIR)):
        if os.path.isdir(os.path.join(ARTICLES_DIR, item)):
            pdfs = [f for f in os.listdir(os.path.join(ARTICLES_DIR, item)) if f.lower().endswith(".pdf")]
            if len(pdfs) > 1:
                print(f"\nAUDITING: {item} ({len(pdfs)} PDFs)", flush=True)
                for pdf in pdfs:
                    pdf_path = os.path.join(ARTICLES_DIR, item, pdf)
                    res = identify_article(client, pdf_path, bib)
                    print(f" - {pdf}: {res.get('id')} | {res.get('title')}", flush=True)

if __name__ == "__main__":
    main()
