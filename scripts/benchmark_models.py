
import os
import base64
import fitz
import json
import argparse
from openai import OpenAI
import re

# Configuration
BENCHMARK_DIR = r"g:\My Drive\Research\Revell\benchmarks"
API_KEY_PATH = r"g:\My Drive\Research\Revell\metadata\openrouter_api_key.txt"

def get_api_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, 'r') as f:
            return f.read().strip()
    return os.environ.get("OPENROUTER_API_KEY")

def pdf_to_base64_images(pdf_path, pages=None, dpi=300):
    """Convert specific PDF pages to base64 images."""
    doc = fitz.open(pdf_path)
    images = {}

    total = len(doc)
    # If pages is None, do all. If pages is a list, do those.
    # pages should be 0-indexed
    target_pages = pages if pages is not None else range(total)

    for p in target_pages:
        if 0 <= p < total:
            page = doc.load_page(p)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            img_data = pix.tobytes("png")
            images[p] = base64.b64encode(img_data).decode('utf-8')
    doc.close()
    return images

def transcribe_with_model(client, model_id, base64_image):
    """Transcribe a single image with a specific model."""
    prompt = (
        "Transcribe the following page image into a TEI P5 XML fragment. "
        "Use appropriate TEI P5 elements such as <pb/> for page breaks (include @n if visible), "
        "<head> for headings, <p> for paragraphs, <note> for footnotes, and <list> for lists. "
        "Preserve all special characters, accents (Hebrew and others), and formatting as accurately as possible. "
        "Return ONLY the XML fragment content (do not include ```xml or other markdown)."
    )

    try:
        response = client.chat.completions.create(
            model=model_id,
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
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR with model {model_id}: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Benchmark multiple OpenRouter models for TEI transcription.")
    parser.add_argument("--input", required=True, help="Path to input PDF.")
    parser.add_argument("--pages", required=True, help="Comma-separated 1-indexed page numbers (e.g. 1,5,10).")
    parser.add_argument("--models", required=True, help="Comma-separated OpenRouter model IDs.")
    parser.add_argument("--tag", default="test", help="Tag for the benchmark run.")

    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("Error: No API key found.")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Process inputs
    page_nums = [int(p.strip()) - 1 for p in args.pages.split(",")] # Convert to 0-indexed
    model_ids = [m.strip() for m in args.models.split(",")]

    if not os.path.exists(BENCHMARK_DIR):
        os.makedirs(BENCHMARK_DIR)

    run_dir = os.path.join(BENCHMARK_DIR, f"run_{args.tag}_{int(os.path.getmtime(args.input))}")
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    print(f"Starting benchmark in {run_dir}...")
    images = pdf_to_base64_images(args.input, pages=page_nums)

    for p_idx in page_nums:
        if p_idx not in images:
            print(f"Skipping page {p_idx+1} (not found in PDF).")
            continue

        img_b64 = images[p_idx]

        for m_id in model_ids:
            print(f"Processing Page {p_idx+1} with Model {m_id}...")
            # Clean model name for filename
            clean_m_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', m_id)
            output_file = os.path.join(run_dir, f"page_{p_idx+1}_{clean_m_name}.xml")

            result = transcribe_with_model(client, m_id, img_b64)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"  Saved to {output_file}")

    print("\nBenchmark complete.")

if __name__ == "__main__":
    main()
