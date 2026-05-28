import sys
import fitz  # PyMuPDF
import difflib
import re

def strip_markdown(text):
    # Basic markdown stripper to ensure difflib doesn't get confused
    text = re.sub(r'[*_#`]', '', text)
    return text.strip()

def process_pdf(bad_pdf_path, clean_md_path, output_path):
    # 1. Load clean text
    with open(clean_md_path, 'r', encoding='utf-8') as f:
        clean_text_raw = f.read()
    clean_text = strip_markdown(clean_text_raw)

    # 2. Extract dirty text and map bounding boxes
    doc = fitz.open(bad_pdf_path)
    dirty_text = ""
    bbox_map = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        words = page.get_text("words") # Returns [x0, y0, x1, y1, "word", block_no, line_no, word_no]
        for w in words:
            word_str = w[4]
            dirty_text += word_str + " "
            # Map each character to this word's bounding box and page
            bbox_map.extend([(page_num, fitz.Rect(w[:4]))] * len(word_str))
            bbox_map.append(None) # Space character
            
    # 3. Align Sequences
    matcher = difflib.SequenceMatcher(None, dirty_text, clean_text)
    opcodes = matcher.get_opcodes()
    
    aligned_data = [] # Stores (page_num, point, clean_word)
    
    for tag, i1, i2, j1, j2 in opcodes:
        if tag in ('equal', 'replace', 'insert'):
            clean_chunk = clean_text[j1:j2]
            if i1 < len(bbox_map) and bbox_map[i1] is not None:
                page_num, rect = bbox_map[i1]
                # Insert at the bottom-left of the original bounding box
                insertion_point = fitz.Point(rect.x0, rect.y1)
                aligned_data.append((page_num, insertion_point, clean_chunk))

    # 4. Create new PDF (Images + Clean Text)
    out_doc = fitz.open()
    for page_num in range(len(doc)):
        old_page = doc[page_num]
        # Render old page to an image to wipe the corrupted text instructions
        pix = old_page.get_pixmap(dpi=300)
        new_page = out_doc.new_page(width=old_page.rect.width, height=old_page.rect.height)
        new_page.insert_image(old_page.rect, pixmap=pix)
        
        # Inject the mapped clean text as invisible (render_mode=3)
        page_texts = [data for data in aligned_data if data[0] == page_num]
        for _, point, text in page_texts:
            new_page.insert_text(point, text, fontname="helv", fontsize=11, render_mode=3)

    out_doc.save(output_path)
    print(f"Success! Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python align.py <input.pdf> <clean.md> <output.pdf>")
        sys.exit(1)
    process_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
