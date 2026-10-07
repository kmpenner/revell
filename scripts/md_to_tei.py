import os
import re
import json
import argparse
from datetime import datetime

def parse_bib_entry(bib_str):
    title = ""
    year = ""
    pages = ""
    volume = ""
    
    # 1. Title is in double quotes
    title_match = re.search(r'\"([^\"]+)\"', bib_str)
    if title_match:
        title = title_match.group(1)
        
    # 2. Year is 4-digit in parenthesis or at end
    year_match = re.search(r'\((\d{4})\)', bib_str)
    if year_match:
        year = year_match.group(1)
    else:
        year_match = re.search(r'\b(\d{4})\b', bib_str)
        if year_match:
            year = year_match.group(1)
            
    # 3. Pages
    pages_match = re.search(r'p\.\s*(\d+[\-\d]*)', bib_str)
    if pages_match:
        pages = pages_match.group(1)
        
    # 4. Volume
    volume_match = re.search(r'Vol\.\s*([A-Za-z0-9_]+)', bib_str)
    if not volume_match:
        volume_match = re.search(r'\b([IVXLCDM]+)\b', bib_str)
    if volume_match:
        volume = volume_match.group(1)
        
    return {
        "title": title or "Unknown Title",
        "year": year or "1990",
        "pages": pages or "",
        "volume": volume or ""
    }

def wrap_hebrew(text):
    # Matches words containing Hebrew characters, pointings, and accents
    # Range \u0590-\u05FF covers Hebrew characters, vowels, and accents.
    # Range \uFB1D-\uFB4F covers Hebrew alphabetic presentation forms.
    hebrew_word_pattern = re.compile(r'([\u0590-\u05FF\uFB1D-\uFB4F]+(?:[/\s\u05BE־]+[\u0590-\u05FF\uFB1D-\uFB4F]+)*)')
    
    # Wrap matches in <foreign xml:lang="he">
    def repl(match):
        val = match.group(1).strip()
        if val:
            return f'<foreign xml:lang="he">{val}</foreign>'
        return match.group(0)
        
    return hebrew_word_pattern.sub(repl, text)

def wrap_brackets_supplied(text):
    # Wrap bracketed Hebrew text in <supplied reason="lost">
    # Matches [ followed by Hebrew characters and optional spaces/punctuation, then ]
    bracketed_pattern = re.compile(r'(\[[^\]]*[\u0590-\u05FF\uFB1D-\uFB4F]+[^\]]*\])')
    return bracketed_pattern.sub(r'<supplied reason="lost">\1</supplied>', text)

def clean_xml_formatting(text):
    # Heuristics for clean TEI P5 elements
    text = re.sub(r'<foreign xml:lang="he">\s*</foreign>', '', text)
    # Fix nested <foreign> tags if any
    text = re.sub(r'<foreign xml:lang="he">\s*<foreign xml:lang="he">', '<foreign xml:lang="he">', text)
    text = re.sub(r'</foreign>\s*</foreign>', '</foreign>', text)
    
    # Standardise damage attributes
    text = re.sub(r'<damage\s+reason=["\']lost["\']', '<damage agent="loss"', text)
    text = re.sub(r'<damage\s+reason=["\']faded["\']', '<damage agent="fading"', text)
    
    # Standardise empty gap tags
    text = re.sub(r'<gap([^>]*?)>\s*</gap>', r'<gap\1 />', text)
    
    return text

def convert_md_to_xml(md_path, bib_data, output_path):
    print(f"Converting {md_path} to {output_path}...")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    # Parse YAML frontmatter
    frontmatter = {}
    body_content = md_content
    if md_content.startswith("---"):
        parts = md_content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body_content = parts[2]
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    frontmatter[k.strip()] = v.strip().strip('"')
                    
    article_id = frontmatter.get("article_id", "")
    bib_key = article_id
    if bib_key.startswith("07a."):
        bib_key = "7.a." + bib_key[4:]
        
    bib_str = bib_data.get(bib_key, "")
    bib_info = parse_bib_entry(bib_str) if bib_str else {"title": frontmatter.get("title", "Unknown Title"), "year": "1990", "pages": "", "volume": ""}
    
    title = bib_info["title"]
    year = bib_info["year"]
    pages = bib_info["pages"]
    volume = bib_info["volume"]
    
    # Build teiHeader
    tei_header = f"""  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>{title}</title>
        <author>
          <persName>
            <forename>E.</forename>
            <forename>J.</forename>
            <surname>Revell</surname>
          </persName>
        </author>
      </titleStmt>
      <publicationStmt>
        <publisher>Haifa University Press</publisher>
        <date when="{year}">{year}</date>
      </publicationStmt>
      <sourceDesc>
        <biblStruct>
          <analytic>
            <title level="a">{title}</title>
            <author>
              <persName>
                <forename>E.</forename>
                <forename>J.</forename>
                <surname>Revell</surname>
              </persName>
            </author>
          </analytic>
          <monogr>
            <title level="j">Masoretic Studies</title>
            <imprint>
              <biblScope unit="volume">{volume}</biblScope>
              <date when="{year}">{year}</date>
              <biblScope unit="page">{pages}</biblScope>
            </imprint>
          </monogr>
        </biblStruct>
      </sourceDesc>
    </fileDesc>
    <profileDesc>
      <langUsage>
        <language ident="en">English</language>
        <language ident="he">Hebrew</language>
      </langUsage>
    </profileDesc>
    <revisionDesc>
      <change>
        <date>{datetime.now().strftime('%Y-%m-%d')}</date>
        <label>Initial TEI transcription creation</label>
      </change>
    </revisionDesc>
  </teiHeader>"""

    # Parse body content page by page (split by form feed \x0c)
    raw_pages = body_content.split('\x0c')
    xml_body = []
    
    current_page_num = None
    
    for i, raw_page in enumerate(raw_pages):
        page_lines = raw_page.splitlines()
        page_lines = [l.strip() for l in page_lines]
        
        # Determine page number
        page_num = None
        for line in page_lines[:5]:
            m = re.match(r'^[—\-\s]*(\d+)[—\-\s]*$', line)
            if m:
                page_num = m.group(1)
                break
        if not page_num:
            for line in reversed(page_lines[-5:]):
                m = re.match(r'^[—\-\s]*(\d+)[—\-\s]*$', line)
                if m:
                    page_num = m.group(1)
                    break
        if not page_num and current_page_num is not None:
            try:
                page_num = str(int(current_page_num) + 1)
            except ValueError:
                pass
                
        if page_num:
            current_page_num = page_num
            pb_tag = f'<pb n="{page_num}"/>'
        else:
            pb_tag = '<pb/>'
            
        xml_body.append(pb_tag)
        
        # Parse paragraphs and headings
        in_list = False
        paragraph_lines = []
        
        for line in page_lines:
            if not line:
                if paragraph_lines:
                    p_text = " ".join(paragraph_lines)
                    if re.match(r'^[—\-\s]*\d+[—\-\s]*$', p_text):
                        paragraph_lines = []
                        continue
                    
                    is_heading = False
                    if p_text.startswith("#"):
                        is_heading = True
                        p_text = p_text.lstrip("#").strip()
                    elif len(p_text) < 80 and (p_text.isupper() or re.match(r'^\d+(\.\d+)*\s+[A-Z]', p_text) or p_text.endswith(":") or "E. J. Revell" in p_text or "University of Toronto" in p_text):
                        is_heading = True
                        
                    p_text = re.sub(r'\*\*([^*]+)\*\*|__([^_]+)__', r'<hi rend="bold">\1\2</hi>', p_text)
                    p_text = re.sub(r'\*([^*]+)\*|_([^_]+)_', r'<hi rend="italic">\1\2</hi>', p_text)
                    
                    p_text = wrap_brackets_supplied(p_text)
                    p_text = wrap_hebrew(p_text)
                    
                    if is_heading:
                        xml_body.append(f'<head>{p_text}</head>')
                    else:
                        xml_body.append(f'<p>{p_text}</p>')
                    paragraph_lines = []
                continue
                
            if line.startswith("- ") or line.startswith("* "):
                if paragraph_lines:
                    p_text = wrap_hebrew(wrap_brackets_supplied(" ".join(paragraph_lines)))
                    xml_body.append(f'<p>{p_text}</p>')
                    paragraph_lines = []
                if not in_list:
                    xml_body.append('<list>')
                    in_list = True
                item_text = wrap_hebrew(wrap_brackets_supplied(line[2:].strip()))
                xml_body.append(f'<item>{item_text}</item>')
                continue
            else:
                if in_list:
                    xml_body.append('</list>')
                    in_list = False
                    
            if "E. J. Revell" in line and len(line) < 30:
                continue
            if "Dehiq" in line and len(line) < 40 and "Exceptions" in line:
                continue
                
            paragraph_lines.append(line)
            
        if paragraph_lines:
            p_text = " ".join(paragraph_lines)
            if not re.match(r'^[—\-\s]*\d+[—\-\s]*$', p_text):
                p_text = wrap_hebrew(wrap_brackets_supplied(p_text))
                xml_body.append(f'<p>{p_text}</p>')
        if in_list:
            xml_body.append('</list>')

    body_str = "\n      ".join(xml_body)
    tei_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
{tei_header}
  <text>
    <body>
      {body_str}
    </body>
  </text>
</TEI>"""

    tei_xml = clean_xml_formatting(tei_xml)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tei_xml)
    print(f"Successfully wrote TEI to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert digitized MD files to TEI XML")
    parser.add_argument("input_md", help="Path to input markdown file")
    parser.add_argument("output_xml", help="Path to output TEI XML file")
    args = parser.parse_args()
    
    bib_path = "metadata/bibliography.json"
    if os.path.exists(bib_path):
        with open(bib_path, 'r', encoding='utf-8') as f:
            bib_data = json.load(f)
    else:
        bib_data = {}
        
    convert_md_to_xml(args.input_md, bib_data, args.output_xml)

if __name__ == "__main__":
    main()
