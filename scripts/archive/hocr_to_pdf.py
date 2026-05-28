import sys
import os
import re
from bs4 import BeautifulSoup
import fitz

def parse_hocr_with_size(hocr_path):
    with open(hocr_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Find page dimensions
    page_div = soup.find('div', class_='ocr_page')
    if not page_div:
         return [], [0, 0, 1000, 1500]
         
    page_title = page_div.get('title', '')
    size_match = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', page_title)
    original_bbox = [int(x) for x in size_match.groups()] if size_match else [0, 0, 1000, 1500]
    
    words = []
    
    # Iterate over lines to handle missing word bboxes
    for line in soup.find_all('span', class_='ocr_line'):
        line_title = line.get('title', '')
        line_match = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', line_title)
        line_bbox = [int(x) for x in line_match.groups()] if line_match else None
        
        line_words = line.find_all('span', class_='ocrx_word')
        
        if not line_words and line_bbox:
            # Maybe the text is directly in the line?
            text = line.get_text().strip()
            if text:
                words.append({'text': text, 'bbox': line_bbox})
            continue

        # Check if words have bboxes
        has_word_bboxes = any(re.search(r'bbox \d+', w.get('title', '')) for w in line_words)
        
        if has_word_bboxes:
            for w in line_words:
                text = w.get_text().strip()
                title = w.get('title', '')
                bbox_match = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', title)
                if bbox_match:
                    words.append({'text': text, 'bbox': [int(x) for x in bbox_match.groups()]})
                elif line_bbox:
                    # Individual word missing bbox, use line bbox as fallback
                    words.append({'text': text, 'bbox': line_bbox})
        elif line_bbox:
            # Distribute words across line bbox
            full_text = " ".join([w.get_text().strip() for w in line_words])
            if not full_text: continue
            
            # Simple proportional distribution
            # Word x-position approximated by character proportion
            total_chars = len(full_text)
            current_char_pos = 0
            line_width = line_bbox[2] - line_bbox[0]
            
            for w in line_words:
                text = w.get_text().strip()
                if not text: continue
                word_len = len(text)
                
                # Approximate start and end based on char position
                x0 = line_bbox[0] + (current_char_pos / total_chars) * line_width
                x1 = line_bbox[0] + ((current_char_pos + word_len) / total_chars) * line_width
                
                word_bbox = [x0, line_bbox[1], x1, line_bbox[3]]
                words.append({'text': text, 'bbox': word_bbox})
                
                current_char_pos += word_len + 1 # +1 for space
                
    return words, original_bbox

def create_pdf(image_path, hocr_path, output_path):
    words, original_bbox = parse_hocr_with_size(hocr_path)
    print(f"Parsed {len(words)} words from HOCR")
    
    img_doc = fitz.open(image_path)
    img_rect = img_doc[0].rect
    width, height = img_rect.width, img_rect.height
    
    scale_x = width / original_bbox[2]
    scale_y = height / original_bbox[3]
    
    doc = fitz.open()
    page = doc.new_page(width=width, height=height)
    page.insert_image(page.rect, filename=image_path)
    
    font_path = r"C:\Windows\Fonts\arial.ttf"
    if os.path.exists(font_path):
        font_name = "arial"
        page.insert_font(fontname=font_name, fontfile=font_path)
    else:
        font_name = "helv"

    for w in words:
        text = w['text']
        bbox = w['bbox']
        r = fitz.Rect(bbox[0]*scale_x, bbox[1]*scale_y, bbox[2]*scale_x, bbox[3]*scale_y)
        font_size = r.height * 0.9
        if font_size <= 0: font_size = 10
        
        try:
           page.insert_text(fitz.Point(r.x0, r.y1), text, fontname=font_name, fontsize=font_size, render_mode=3)
        except Exception as e:
           pass
        
    doc.save(output_path)
    print(f"Success! Created PDF at {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python hocr_to_pdf.py <image_path> <hocr_path> <output_path>")
        sys.exit(1)
    
    create_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
