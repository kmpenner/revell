import fitz
import sys
import os

def fix_pdf_page(input_path, output_path):
    print(f"Processing all pages in {input_path}...")
    doc = fitz.open(input_path)
    
    for i, page in enumerate(doc):
        print(f"  Processing page {i+1}...")
        
        # 1. Get content bounding box to crop blank space
        text_blocks = page.get_text("blocks")
        text_bbox = None
        if text_blocks:
            x0, y0, x1, y1 = text_blocks[0][:4]
            for b in text_blocks[1:]:
                x0 = min(x0, b[0])
                y0 = min(y0, b[1])
                x1 = max(x1, b[2])
                y1 = max(y1, b[3])
            text_bbox = fitz.Rect(x0, y0, x1, y1)

        # 2. If no text, try images
        if not text_bbox:
            images = page.get_image_info(hashes=False)
            if images:
                x0, y0, x1, y1 = images[0]["bbox"]
                for img in images[1:]:
                    x0 = min(x0, img["bbox"][0])
                    y0 = min(y0, img["bbox"][1])
                    x1 = max(x1, img["bbox"][2])
                    y1 = max(y1, img["bbox"][3])
                text_bbox = fitz.Rect(x0, y0, x1, y1)

        if text_bbox:
            # Increase margin to 72 points (1 inch) for a "normal book" look
            margin = 72
            new_rect = text_bbox + (-margin, -margin, margin, margin)
            new_rect.intersect(page.rect)
            page.set_cropbox(new_rect)
        else:
            print(f"  No content found on page {i+1}.")

        # 3. Rotate 0 degrees (Portrait)
        # If the pages are already right-side up, 0 ensures portrait orientation.
        page.set_rotation(0)

    doc.save(output_path)
    doc.close()
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python fix_pdf_page.py <input_pdf> <output_pdf>")
    else:
        fix_pdf_page(sys.argv[1], sys.argv[2])
