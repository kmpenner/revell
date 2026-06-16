
import os
import io
import json
import base64
import argparse
import logging
import fitz  # PyMuPDF
from PIL import Image
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
ASSETS_IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images", "articles")
API_KEY_PATH = os.path.join(ROOT_DIR, "metadata", "openrouter_api_key.txt")

def get_api_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, 'r') as f:
            return f.read().strip()
    return os.environ.get("OPENROUTER_API_KEY")

def pdf_page_to_base64(pdf_path, page_num, dpi=300):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
    img_data = pix.tobytes("png")
    doc.close()
    return base64.b64encode(img_data).decode('utf-8'), pix.width, pix.height

def detect_bounds(client, base64_image, model="google/gemini-2.0-flash-001"):
    prompt = (
        "Detect the bounding box of the physical sheet of paper (the page) in this image. "
        "The bounding box MUST include all margins, page numbers, headers, and any handwritten notes or marginalia. "
        "It should encompass everything that is part of the paper itself, excluding only the scanner bed or background outside the paper edges. "
        "Return the coordinates as a JSON object with keys [ymin, xmin, ymax, xmax]. "
        "The coordinates should be normalized from 0 to 1000. "
        "Return ONLY the JSON object."
    )

    try:
        response = client.chat.completions.create(
            model=model,
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
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        logging.error(f"Error detecting bounds: {e}")
        return None

def process_pdf(pdf_path, article_id, client):
    article_img_dir = os.path.join(ASSETS_IMAGES_DIR, article_id)
    if not os.path.exists(article_img_dir):
        os.makedirs(article_img_dir)

    doc = fitz.open(pdf_path)
    num_pages = len(doc)

    logging.info(f"Processing {article_id} ({num_pages} pages)...")

    for page_num in range(num_pages):
        output_path = os.path.join(article_img_dir, f"page_{page_num+1}.png")
        # We overwrite to re-test
        # if os.path.exists(output_path):
        #     logging.info(f"  Page {page_num+1} already exists, skipping.")
        #     continue

        logging.info(f"  Extracting page {page_num+1} (cropping disabled)...")
        try:
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            pix.save(output_path)
            logging.info(f"    Saved original page to {output_path}")
        except Exception as e:
            logging.error(f"    Error extracting page {page_num+1}: {e}")
    doc.close()

def main():
    parser = argparse.ArgumentParser(description="Batch extract and crop PDF pages.")
    parser.add_argument("--article", help="Optional article ID to process (e.g. 07a.03)")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        logging.error("No API key found.")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Iterate through article folders
    for folder in sorted(os.listdir(ARTICLES_DIR)):
        folder_path = os.path.join(ARTICLES_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        # Extract ID (e.g. 07a.01)
        if not folder.startswith("07a."):
            continue
        article_id = folder.split(" - ")[0]

        if args.article and article_id != args.article:
            continue

        # Find PDFs in the folder
        pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        for pdf_file in pdfs:
            pdf_path = os.path.join(folder_path, pdf_file)
            # Use filename as sub-identifier if multiple PDFs (e.g. p1, p2)
            if len(pdfs) > 1:
                pdf_id = f"{article_id}_{os.path.splitext(pdf_file)[0]}"
            else:
                pdf_id = article_id

            process_pdf(pdf_path, pdf_id, client)

if __name__ == "__main__":
    main()
