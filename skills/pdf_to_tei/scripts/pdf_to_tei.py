
import os
import io
import base64
import argparse
import json
import re
import fitz  # PyMuPDF
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pdf_to_base64_images(pdf_path, dpi=300):
    """Convert PDF pages to base64 encoded images."""
    logging.info(f"Converting PDF to images: {pdf_path}")
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        img_data = pix.tobytes("png")
        base64_image = base64.b64encode(img_data).decode('utf-8')
        images.append(base64_image)
    doc.close()
    return images

def get_citation(pdf_path):
    """Try to find bibliographic info for the given PDF."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Walk up to find Revell root if needed, but we assume it's running in typical structure
    bib_path = os.path.join(root_dir, "metadata", "bibliography.json")
    if not os.path.exists(bib_path):
        bib_path = r"g:\My Drive\Research\Revell\metadata\bibliography.json"

    # Extract ID from filename/folder
    # Pattern: 07a.01
    filename = os.path.basename(pdf_path)
    match = re.search(r'(\d+[a-z]?)\.(\d+)', filename)
    if not match:
        # Try folder name
        parent = os.path.basename(os.path.dirname(pdf_path))
        match = re.search(r'(\d+[a-z]?)\.(\d+)', parent)

    if match:
        # Convert 07a.01 to 7.a.01 (as seen in CV JSON)
        sec, num = match.groups()
        sec_fmt = ".".join(list(sec.lstrip('0'))) # 07a -> 7.a
        id_query = f"{sec_fmt}.{num}"

        if os.path.exists(bib_path):
            with open(bib_path, 'r', encoding='utf-8') as f:
                bib = json.load(f)
            return id_query, bib.get(id_query) or bib.get(f"7.a.{num}") # Fallback to 7.a

    return None, None

def generate_header(client, citation, filename, model="qwen/qwen3.6-flash"):
    """Generate a high-quality TEI Header based on bibliographic info."""
    prompt = f"""
    Create a complete <teiHeader> for the following scholarly article.
    Citation: {citation}
    Filename: {filename}

    The author is E. J. Revell.
    Extract the title, journal/book title, date, volume, and pages from the citation.
    Return ONLY the <teiHeader> XML block.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```xml"):
        content = content[6:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
    return content

def transcribe_page(client, base64_image, model="qwen/qwen3.6-flash"):
    """Send image to OpenRouter for transcription."""
    prompt = (
        "Transcribe the following page image into a TEI P5 XML fragment. "
        "Use appropriate TEI P5 elements such as <pb/> for page breaks (include @n if visible), "
        "<head> for headings, <p> for paragraphs, <note> for footnotes, and <list> for lists. "
        "Preserve all special characters, accents, and formatting as accurately as possible. "
        "Return ONLY the XML fragment content (do not include ```xml or other markdown)."
    )

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
        max_tokens=4096
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```xml"):
        content = content[6:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
    return content

def escape_invalid_tags(xml_text):
    valid_tags = {
        'p', 'pb', 'head', 'list', 'item', 'note', 'ref', 'lb', 'hi',
        'teiHeader', 'fileDesc', 'titleStmt', 'title', 'publicationStmt', 'sourceDesc',
        'text', 'body', 'TEI', 'div', 'table', 'row', 'cell', 'num', 'g', 'cb', 'sup', 'em',
        '/p', '/head', '/list', '/item', '/note', '/ref', '/lb', '/hi',
        '/teiHeader', '/fileDesc', '/titleStmt', '/title', '/publicationStmt', '/sourceDesc',
        '/text', '/body', '/TEI', '/div', '/table', '/row', '/cell', '/num', '/g', '/cb', '/sup', '/em'
    }
    
    def replace_tag(match):
        tag = match.group(0)
        if tag.startswith('<?xml') or tag.startswith('<?XML') or tag.startswith('<!--'):
            return tag
            
        tag_name_match = re.match(r'^</?([a-zA-Z0-9_:-]+)', tag)
        if tag_name_match:
            name = tag_name_match.group(1)
            if name in valid_tags or ('/' + name) in valid_tags:
                return tag
        return tag.replace('<', '&lt;').replace('>', '&gt;')
        
    return re.sub(r'<[^>]+>', replace_tag, xml_text)

def clean_xml_content(xml_text):
    # Fix common tag spacing/spelling typos from LLM
    xml_text = re.sub(r'<hirend=', '<hi rend=', xml_text)
    xml_text = re.sub(r'<pbn=', '<pb n=', xml_text)
    xml_text = re.sub(r'<notetype=', '<note type=', xml_text)
    xml_text = re.sub(r'<reftarget=', '<ref target=', xml_text)
    
    # Strip duplicate XML declarations from fragments
    lines = xml_text.splitlines()
    cleaned_lines = []
    xml_decl_found = False
    for line in lines:
        if '<?xml' in line:
            if not xml_decl_found:
                cleaned_lines.append(line)
                xml_decl_found = True
        else:
            cleaned_lines.append(line)
            
    xml_text = escape_invalid_tags('\n'.join(cleaned_lines))
    return fix_semantic_anomalies(xml_text)

def fix_semantic_anomalies(xml_text):
    """Post-processing heuristic fixes for LLM OCR anomalies."""
    # 1. Strip watermarks
    xml_text = re.sub(r'(?i)\s*Digitized by Google\s*', '', xml_text)
    
    # 2. Fix floating page numbers (e.g. "— 84 —")
    # Matches <p>— 84 —</p> or just — 84 — on its own line
    xml_text = re.sub(r'(?m)^[—\-]\s*(\d+)\s*[—\-]$', r'<pb n="\1"/>', xml_text)
    xml_text = re.sub(r'<p>\s*[—\-]\s*(\d+)\s*[—\-]\s*</p>', r'<pb n="\1"/>', xml_text)

    # 3. Normalize <pb> sequences
    pb_tags = list(re.finditer(r'<pb[^>]*>', xml_text))
    
    first_num = None
    first_num_idx = -1
    for i, match in enumerate(pb_tags):
        tag_text = match.group(0)
        n_match = re.search(r'n=["\'](\d+)["\']', tag_text)
        if n_match:
            first_num = int(n_match.group(1))
            first_num_idx = i
            break
            
    if first_num is not None:
        # Calculate the starting number for the very first pb tag
        start_num = first_num - first_num_idx
        current_num = start_num
        
        def replace_pb(match):
            nonlocal current_num
            replacement = f'<pb n="{current_num}"/>'
            current_num += 1
            return replacement
            
        xml_text = re.sub(r'<pb[^>]*>', replace_pb, xml_text)
        
    return xml_text


def main():
    parser = argparse.ArgumentParser(description="Transcribe PDF to TEI P5 XML using OpenRouter and Qwen 3.6 Flash.")
    parser.add_argument("--input", required=True, help="Path to input PDF file.")
    parser.add_argument("--output", required=True, help="Path to output XML file.")
    parser.add_argument("--model", default="qwen/qwen3.6-flash", help="OpenRouter model ID.")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set.")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    try:
        # Get metadata
        article_id, citation = get_citation(args.input)
        if citation:
            logging.info(f"Found citation for {article_id}: {citation}")
            header = generate_header(client, citation, os.path.basename(args.input), model=args.model)
        else:
            logging.warning("No citation found in bibliography.json. Using generic header.")
            header = f"""
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Transcription of {os.path.basename(args.input)}</title>
      </titleStmt>
      <publicationStmt>
        <p>Digitized as part of the Revell Digital Corpus Project.</p>
      </publicationStmt>
      <sourceDesc>
        <p>Original PDF: {os.path.basename(args.input)}</p>
      </sourceDesc>
    </fileDesc>
  </teiHeader>"""

        images = pdf_to_base64_images(args.input)
        tei_fragments = []

        for i, img in enumerate(images):
            logging.info(f"Transcribing page {i+1}/{len(images)}...")
            fragment = transcribe_page(client, img, model=args.model)
            tei_fragments.append(fragment)

        # Basic TEI structure
        tei_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<TEI xmlns="http://www.tei-c.org/ns/1.0">\n'
            f'{header}\n'
            '  <text>\n'
            '    <body>\n'
            '      ' + '\n      '.join(tei_fragments) + '\n'
            '    </body>\n'
            '  </text>\n'
            '</TEI>'
        )

        tei_xml = clean_xml_content(tei_xml)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(tei_xml)
        print(f"Transcription complete: {args.output}")

    except Exception as e:
        logging.error(f"Failed to process PDF: {e}")

if __name__ == "__main__":
    main()
