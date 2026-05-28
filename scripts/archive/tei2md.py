import sys
import re
from bs4 import BeautifulSoup

def tei_to_markdown(tei_path, md_path):
    with open(tei_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')

    # Start with the body
    body = soup.find('body')
    if not body:
        print("Error: No <body> found in TEI file.")
        return

    md_lines = []

    note_count = 0

    def process_element(element):
        nonlocal note_count
        if element.name == 'p':
            content = process_children(element)
            md_lines.append(f"\n{content}\n")
        elif element.name == 'head':
            content = process_children(element)
            # Find heading level
            level = 1
            parent = element.parent
            while parent and parent.name != 'body':
                if parent.name in ['div', 'list']:
                    level += 1
                parent = parent.parent
            md_lines.append(f"\n{'#' * min(level, 6)} {content}\n")
        elif element.name == 'list':
            for item in element.find_all('item', recursive=False):
                content = process_children(item)
                md_lines.append(f"\n* {content}")
            md_lines.append("\n") # newline after list
        elif element.name == 'lb':
            md_lines.append("\n")
        elif element.name == 'pb':
            md_lines.append("\n---\n")
        elif element.name == 'hi':
            content = process_children(element)
            rend = element.get('rend') or element.get('rendition')
            if rend and 'italic' in rend:
                md_lines.append(f" *{content}* ")
            elif rend and 'bold' in rend:
                md_lines.append(f" **{content}** ")
            else:
                md_lines.append(f" {content} ")
        elif element.name == 'foreign':
            content = process_children(element)
            md_lines.append(f" {content} ")
        elif element.name == 'note':
            note_count += 1
            content = process_children(element)
            # Add superscript in text and footnote at end? 
            # Or just inline for now but with unique ID
            md_lines.append(f" [^note{note_count}]")
            md_lines.append(f"\n\n[^note{note_count}]: {content}\n\n")
        elif element.name == 'ref':
            content = process_children(element)
            md_lines.append(f" [{content}] ")
        elif element.name == 'figure':
            desc = element.find('figDesc')
            if desc:
                md_lines.append(f"\n> [Figure: {desc.get_text().strip()}]\n")
        elif element.name == 'graphic':
            url = element.get('url')
            md_lines.append(f" ![Image]({url}) ")
        else:
            # For unknown tags, just process children
            md_lines.append(process_children(element))

    def process_children(element):
        parts = []
        for child in element.children:
            if isinstance(child, str):
                # Keep spaces but strip newlines
                text = child.replace('\n', ' ').replace('\r', '')
                parts.append(text)
            elif child.name:
                if child.name in ['hi', 'foreign', 'lb', 'ref', 'note', 'emph']:
                    if child.name in ['hi', 'emph']:
                        content = process_children(child)
                        rend = child.get('rend') or child.get('rendition')
                        if (rend and ('italic' in rend)) or child.name == 'emph':
                            parts.append(f" *{content}* ")
                        elif rend and 'bold' in rend:
                            parts.append(f" **{content}** ")
                        else:
                            parts.append(f" {content} ")
                    elif child.name == 'foreign':
                        parts.append(f" {process_children(child)} ")
                    elif child.name == 'lb':
                        parts.append("\n")
                    elif child.name == 'ref':
                        parts.append(f" [{process_children(child)}] ")
                    elif child.name == 'note':
                        nonlocal note_count
                        note_count += 1
                        note_content = process_children(child)
                        parts.append(f" [^note{note_count}] ")
                        md_lines.append(f"\n\n[^note{note_count}]: {note_content}\n\n")
                else:
                    parts.append(child.get_text().strip())
        return re.sub(r' +', ' ', "".join(parts)).strip()

    # Actually we should walk the tree
    for child in body.children:
        if child.name:
            process_element(child)

    # Join and clean up double spaces/newlines
    final_md = "".join(md_lines)
    # Basic cleanup: remove redundant 
    final_md = re.sub(r'\n{3,}', '\n\n', final_md)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(final_md.strip())
    print(f"Successfully converted {tei_path} to {md_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tei2md.py <input_tei.xml> [output_md.md]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.xml', '.md')
    tei_to_markdown(input_file, output_file)
