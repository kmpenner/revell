import os
import sys as _sys, os as _os
# scripts/markdown.py shadows the Python-Markdown library; import the real one.
_here = _os.path.dirname(_os.path.abspath(__file__))
_sys.path = [p for p in _sys.path if _os.path.abspath(p or '.') != _here]
import markdown
_sys.path.insert(0, _here)
import shutil
import glob
import re
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, "docs")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")

# --- CSS / DESIGN ---
CSS_CONTENT = """
:root {
    --primary-color: #2c3e50;
    --secondary-color: #34495e;
    --accent-color: #3498db;
    --text-color: #333;
    --bg-color: #fdfdfd;
    --header-bg: #fff;
    --border-color: #eaeaea;
    --font-heading: 'Merriweather', serif;
    --font-body: 'Roboto', sans-serif;
}

body {
    font-family: var(--font-body);
    color: var(--text-color);
    background-color: var(--bg-color);
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

a { color: var(--accent-color); text-decoration: none; transition: color 0.2s; }
a:hover { color: #2980b9; text-decoration: underline; }

.wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    background: #fff;
    box-shadow: 0 0 20px rgba(0,0,0,0.05);
    min-height: 100vh;
}

header {
    text-align: center;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2rem;
    padding-bottom: 2rem;
}

header h1 {
    font-family: var(--font-heading);
    margin: 0 0 0.5rem 0;
    font-size: 2.5rem;
    color: var(--primary-color);
}

header h1 a { color: inherit; text-decoration: none; }
header p { color: #7f8c8d; font-style: italic; margin: 0; }

nav ul {
    padding: 0;
    margin: 1.5rem 0 0 0;
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 2rem;
}

nav li a {
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
    color: var(--secondary-color);
}

/* Side-by-Side Layout */
.edition-container {
    display: flex;
    gap: 2rem;
    align-items: flex-start;
}

.transcription-pane {
    flex: 1;
    min-width: 0;
}

.facsimile-pane {
    flex: 1;
    position: sticky;
    top: 2rem;
    border: 1px solid var(--border-color);
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 4px;
}

.facsimile-pane img {
    width: 100%;
    height: auto;
    display: block;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.facsimile-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

article header {
    text-align: left;
    border-bottom: none;
    margin-bottom: 2rem;
    padding-bottom: 0;
}

article h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-family: var(--font-heading);
}

.meta {
    color: #95a5a6;
    font-size: 0.85rem;
    margin-bottom: 0.2rem;
}

.tei-link {
    color: var(--accent-color);
    font-weight: bold;
    margin-right: 0.5rem;
    border: 1px solid #d1e2ff;
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    background: #f1f8ff;
    font-size: 0.8rem;
    display: inline-block;
    transition: all 0.2s;
}
.tei-link:hover {
    background: var(--accent-color);
    color: #fff;
    text-decoration: none;
}

.content {
    font-size: 1.1rem;
    text-align: justify;
}

.content h2 { margin-top: 2rem; color: var(--primary-color); font-family: var(--font-heading); border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }
.content h3 { margin-top: 1.5rem; color: var(--secondary-color); font-family: var(--font-heading); }
.content blockquote { border-left: 4px solid var(--accent-color); margin: 1.5rem 0; padding-left: 1rem; color: #555; background: #f9f9f9; padding: 1rem; font-style: italic; }

.hebrew {
    font-family: 'SBL Hebrew', 'Arial', sans-serif;
    font-size: 1.25rem;
    direction: rtl;
    unicode-bidi: embed;
}
.footnote-ref {
    font-size: 0.75rem;
    vertical-align: super;
    line-height: 0;
    margin-left: 2px;
}
.footnote-ref a {
    color: var(--accent-color);
    font-weight: bold;
}
.page-break {
    border-top: 1px dashed #ccc;
    color: #999;
    font-size: 0.8rem;
    text-align: center;
    margin: 2rem 0;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.unclear {
    border-bottom: 1px dotted #888;
    color: #555;
}
.item-num {
    font-weight: bold;
    margin-right: 0.5rem;
    color: var(--secondary-color);
}
.item-label {
    font-weight: bold;
    color: var(--primary-color);
}
.footnotes {
    margin-top: 3rem;
    font-size: 0.95rem;
}
.footnotes hr {
    border: 0;
    border-top: 1px solid var(--border-color);
}
.footnotes h3 {
    font-family: var(--font-heading);
    color: var(--primary-color);
}
.footnotes ol {
    padding-left: 1.5rem;
}
.footnotes li {
    margin-bottom: 0.5rem;
}
.footnote-backref {
    color: var(--accent-color);
    margin-left: 0.3rem;
    font-weight: bold;
    text-decoration: none;
}

footer {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    text-align: center;
    color: #bdc3c7;
    font-size: 0.8rem;
}

ul.article-list { list-style: none; padding: 0; }
ul.article-list li { margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px dashed #eee; }
ul.article-list li a { font-weight: bold; font-size: 1.2rem; display: block; font-family: var(--font-heading); }
"""

# --- HTML TEMPLATES ---
BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Revell Digital Corpus</title>
    <link rel="stylesheet" href="{css_path}">
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --font-heading: 'Merriweather', serif;
            --font-body: 'Roboto', sans-serif;
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <header>
            <h1><a href="{root_path}index.html">Revell Digital Corpus</a></h1>
            <p>A TEI Edition of Ernest John Revell’s Collected Essays</p>
            <nav>
                <ul>
                    <li><a href="{root_path}index.html">Home</a></li>
                    <li><a href="{root_path}articles.html">Articles</a></li>
                    <li><a href="{root_path}books.html">Books</a></li>
                    <li><a href="{root_path}biography.html">Biography</a></li>
                    <li><a href="{root_path}search.html">Search</a></li>
                </ul>
            </nav>
        </header>
        <section>
            {content}
        </section>
        <footer>
            <p><small>Generated on {date} &mdash; Static Site</small></p>
        </footer>
    </div>
</body>
</html>
"""

ARTICLE_TEMPLATE = """
<article>
    <div class="edition-container">
        <div class="transcription-pane">
            <header>
                <h1>{title}</h1>
                {meta_html}
            </header>
            <div class="content">
                {content}
            </div>
        </div>
        {facsimile_html}
    </div>
</article>
"""

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def safe_copy(src, dst):
    try:
        shutil.copy2(src, dst)
    except Exception:
        try:
            shutil.copy(src, dst)
        except Exception:
            shutil.copyfile(src, dst)

def compress_pdf(src_path, dest_path):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        try:
            if os.path.getmtime(dest_path) >= os.path.getmtime(src_path):
                return True
        except Exception:
            pass

    import subprocess
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={dest_path}",
        src_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
            return True
    except Exception as e:
        pass
    
    safe_copy(src_path, dest_path)
    return False

def fix_links(html_content):
    # Regex to replace .md and .xml links with .html
    html_content = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html_content)
    return re.sub(r'href="([^"]+)\.xml"', r'href="\1.html"', html_content)

def convert_md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Strip Jekyll-style front matter (the meta extension misses it after a leading blank line)
    front = {}
    m = re.match(r'\s*---\s*\n(.*?)\n---\s*\n', text, re.S)
    if m:
        front = dict(l.split(':', 1) for l in m.group(1).splitlines() if ':' in l)
        front = {k.strip(): v.strip() for k, v in front.items()}
        text = text[m.end():]

    md = markdown.Markdown(extensions=['meta', 'fenced_code', 'tables'])
    html_content = md.convert(text)

    # Fix links in the content
    html_content = fix_links(html_content)

    meta = md.Meta if hasattr(md, 'Meta') else {}
    flattened_meta = {k: v[0] if isinstance(v, list) and v else "" for k, v in meta.items()}
    flattened_meta.update(front)

    return html_content, flattened_meta

def convert_tei_to_html(xml_path):
    from html.parser import HTMLParser
    
    class TEIParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.output_parts = []
            self.footnotes = []
            
            # Metadata
            self.title_chunks = []
            self.date_chunks = []
            self.title_captured = False
            self.date_captured = False
            
            # States
            self.in_header = False
            self.in_title_stmt = False
            self.in_title = False
            self.in_publication_stmt = False
            self.in_imprint = False
            self.in_date = False
            
            # Footnote capture
            self.in_note = False
            self.note_depth = 0
            self.current_note_id = None
            self.current_note_buffer = []
            
            # HTML tag tracking stack
            self.tag_stack = []

        def handle_starttag(self, tag, attrs):
            attr_dict = dict(attrs)
            
            # Metadata tracking
            if tag == 'titlestmt':
                self.in_title_stmt = True
            elif tag == 'title' and self.in_title_stmt and not self.title_captured:
                self.in_title = True
            elif tag == 'publicationstmt':
                self.in_publication_stmt = True
            elif tag == 'imprint':
                self.in_imprint = True
            elif tag == 'date' and (self.in_publication_stmt or self.in_imprint) and not self.date_captured:
                self.in_date = True
            elif tag == 'teiheader':
                self.in_header = True

            if self.in_header:
                return
                
            if tag == 'note':
                self.in_note = True
                self.current_note_id = attr_dict.get('n') or attr_dict.get('xml:id') or str(len(self.footnotes) + 1)
                self.current_note_buffer = []
                return

            # If inside a footnote note tag, buffer the raw content
            if self.in_note:
                attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
                self.current_note_buffer.append(f"<{tag}{attr_str}>")
                return

            # Main content tag translation
            html_start = ""
            if tag == 'p':
                html_start = "<p>"
            elif tag == 'head':
                html_start = "<h2>"
            elif tag in ['hi', 'i', 'emphasis', 'emph', 'term']:
                rend = attr_dict.get('rend') or attr_dict.get('rendition')
                if rend == 'bold':
                    html_start = "<b>"
                elif rend == 'typewriter':
                    html_start = "<code>"
                elif rend in ['sup', 'superscript']:
                    html_start = "<sup>"
                elif rend == 'underline':
                    html_start = "<u>"
                else:
                    html_start = "<i>"
            elif tag == 'foreign':
                lang = attr_dict.get('lang') or attr_dict.get('xml:lang') or attr_dict.get('{http://www.w3.org/XML/1998/namespace}lang')
                if lang in ['he', 'heb']:
                    html_start = '<span dir="rtl" class="hebrew">'
                else:
                    html_start = '<i>'
            elif tag == 'pb':
                pb_n = attr_dict.get('n')
                if pb_n:
                    html_start = f'<div class="page-break" id="page-{pb_n}">[Page {pb_n}]</div>'
                else:
                    html_start = '<div class="page-break">[Page Break]</div>'
            elif tag == 'lb':
                html_start = "<br/>"
            elif tag == 'list':
                html_start = "<ul>\n"
            elif tag == 'item':
                item_n = attr_dict.get('n')
                if item_n:
                    html_start = f'<li><span class="item-num">{item_n}</span> '
                else:
                    html_start = "<li>"
            elif tag == 'label':
                html_start = '<span class="item-label">'
            elif tag == 'unclear':
                html_start = '<span class="unclear" title="Unclear text">'
            elif tag == 'fw':
                html_start = '<span class="fw">'
            elif tag == 'space':
                qty = attr_dict.get('quantity') or "1"
                try:
                    spaces = "&nbsp;" * int(qty)
                except ValueError:
                    spaces = "&nbsp;"
                html_start = spaces

            if html_start:
                self.output_parts.append(html_start)
                self.tag_stack.append((tag, html_start))

        def handle_endtag(self, tag):
            if tag == 'titlestmt':
                self.in_title_stmt = False
            elif tag == 'title' and self.in_title:
                self.in_title = False
                self.title_captured = True
            elif tag == 'publicationstmt':
                self.in_publication_stmt = False
            elif tag == 'imprint':
                self.in_imprint = False
            elif tag == 'date' and self.in_date:
                self.in_date = False
                self.date_captured = True
            elif tag == 'teiheader':
                self.in_header = False
                return

            if self.in_header:
                return

            if tag == 'note' and self.in_note:
                self.in_note = False
                note_content = "".join(self.current_note_buffer).strip()
                self.footnotes.append((self.current_note_id, note_content))
                self.output_parts.append(f'<sup class="footnote-ref"><a href="#fn-{self.current_note_id}" id="fnref-{self.current_note_id}">{self.current_note_id}</a></sup>')
                return

            if self.in_note:
                self.current_note_buffer.append(f"</{tag}>")
                return

            # Pop tags from stack to close them
            html_close = ""
            for i in range(len(self.tag_stack) - 1, -1, -1):
                stack_tag, html_start = self.tag_stack[i]
                if stack_tag == tag:
                    if html_start.startswith("<p>"): html_close = "</p>\n"
                    elif html_start.startswith("<h2>"): html_close = "</h2>\n"
                    elif html_start.startswith("<b>"): html_close = "</b>"
                    elif html_start.startswith("<code>"): html_close = "</code>"
                    elif html_start.startswith("<sup>"): html_close = "</sup>"
                    elif html_start.startswith("<u>"): html_close = "</u>"
                    elif html_start.startswith("<i>"): html_close = "</i>"
                    elif html_start.startswith('<span dir="rtl" class="hebrew">'): html_close = "</span>"
                    elif html_start.startswith("<ul>"): html_close = "</ul>\n"
                    elif html_start.startswith("<li>"): html_close = "</li>\n"
                    elif html_start.startswith('<span class="item-label">'): html_close = "</span>"
                    elif html_start.startswith('<span class="unclear"'): html_close = "</span>"
                    elif html_start.startswith('<span class="fw">'): html_close = "</span>"
                    
                    del self.tag_stack[i:]
                    break

            if html_close:
                self.output_parts.append(html_close)

        def handle_data(self, data):
            if self.in_title:
                self.title_chunks.append(data)
            elif self.in_date:
                self.date_chunks.append(data)
            
            if self.in_note:
                self.current_note_buffer.append(data)
            elif not self.in_header:
                self.output_parts.append(data)

        def handle_entityref(self, name):
            ref = f"&{name};"
            if self.in_note:
                self.current_note_buffer.append(ref)
            elif not self.in_header:
                self.output_parts.append(ref)

        def handle_charref(self, name):
            ref = f"&#{name};"
            if self.in_note:
                self.current_note_buffer.append(ref)
            elif not self.in_header:
                self.output_parts.append(ref)

    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
            
        parser = TEIParser()
        parser.feed(xml_content)
        
        content_html = "".join(parser.output_parts).strip()
        footnotes = parser.footnotes
        title = "".join(parser.title_chunks).strip()
        date = "".join(parser.date_chunks).strip()
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
        return "", {}

    # Extract article ID from path (e.g. '07a.01')
    article_id = ""
    match = re.search(r'07a\.\d+', xml_path)
    if match:
        article_id = match.group(0)

    # Clean title
    if title:
        if title.startswith("Transcription of "):
            title = title[len("Transcription of "):]
        if title.endswith(".pdf"):
            title = title[:-4]
        title = title.replace('_', ' ').replace('-', ' ')
    
    # Fallback to heading in text if title is not set
    if not title:
        match_head = re.search(r'<h2>(.*?)</h2>', content_html)
        if match_head:
            title = re.sub(r'<[^>]+>', '', match_head.group(1)).strip().replace('\n', ' ')
            
    if not title:
        title = os.path.basename(os.path.dirname(xml_path))

    # Append footnotes
    if footnotes:
        content_html += '\n<div class="footnotes"><hr><h3>Footnotes</h3><ol>\n'
        for note_id, note_content in footnotes:
            content_html += f'<li id="fn-{note_id}">{note_content} <a href="#fnref-{note_id}" class="footnote-backref">↩</a></li>\n'
        content_html += '</ol></div>\n'

    meta = {
        'title': title,
        'article_id': article_id,
        'date': date
    }
    return content_html, meta

def generate_page(output_path, title, content, depth=0):
    root_path = "../" * depth if depth > 0 else ""
    css_path = f"{root_path}assets/css/style.css"

    # Fix links in the full page content
    content = fix_links(content)

    page_html = BASE_TEMPLATE.format(
        title=title,
        content=content,
        root_path=root_path,
        css_path=css_path,
        date=datetime.now().strftime("%Y-%m-%d")
    )
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"Generated {output_path}")

def main():
    ensure_dir(OUTPUT_DIR)

    # Clean only HTML and XML files in OUTPUT_DIR to preserve compressed PDFs
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(".html") or file.endswith(".xml"):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass

    # Gather PDF compression tasks
    pdf_tasks = []
    
    # 1. Articles PDFs
    article_files = glob.glob(os.path.join(ARTICLES_DIR, "**/*.xml"), recursive=True)
    articles_out_dir = os.path.join(OUTPUT_DIR, "articles")
    ensure_dir(articles_out_dir)
    
    for xml_path in article_files:
        filename = os.path.basename(xml_path)
        if not filename.startswith("transcription"):
            continue
        src_dir = os.path.dirname(xml_path)
        pdfs = [f for f in os.listdir(src_dir) if f.lower().endswith(".pdf") and "reject" not in f.lower()]
        if pdfs:
            pdfs.sort()
            pdf_name = pdfs[0]
            src_pdf = os.path.join(src_dir, pdf_name)
            dest_pdf = os.path.join(articles_out_dir, pdf_name)
            pdf_tasks.append((src_pdf, dest_pdf))

    # 2. Books PDFs
    bib_path = os.path.join(ROOT_DIR, "metadata", "bibliography.json")
    bib_data = {}
    if os.path.exists(bib_path):
        import json
        with open(bib_path, 'r', encoding='utf-8') as f:
            bib_data = json.load(f)
        
        books_out_dir = os.path.join(OUTPUT_DIR, "books")
        ensure_dir(books_out_dir)
        
        books = sorted([(k, v) for k, v in bib_data.items() if k.startswith("7.b.")])
        books_src_dir = os.path.join(ROOT_DIR, "07b Books")
        if os.path.exists(books_src_dir):
            book_pdf_files = []
            for root, dirs, files in os.walk(books_src_dir):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        book_pdf_files.append((root, file))
            
            for book_id, citation in books:
                book_num = int(book_id.split(".")[-1])
                pdf_name = f"{book_id}.pdf"
                pdf_path = None
                for root, file in book_pdf_files:
                    parent_folder = os.path.basename(root)
                    if (parent_folder.startswith(f"07b.{book_num}") or 
                        file.startswith(f"07b.{book_num}") or 
                        file.startswith(f"7.b.{book_num}") or 
                        file.startswith(f"Revell 07b.{book_num}")):
                        pdf_path = os.path.join(root, file)
                        break
                if pdf_path:
                    dest_pdf = os.path.join(books_out_dir, pdf_name)
                    pdf_tasks.append((pdf_path, dest_pdf))

    # Compress PDFs in parallel
    pdf_tasks = list(set(pdf_tasks))
    if pdf_tasks:
        from concurrent.futures import ThreadPoolExecutor
        print(f"Processing {len(pdf_tasks)} unique PDFs in parallel...")
        def compress_worker(task):
            src, dest = task
            try:
                compress_pdf(src, dest)
            except Exception as e:
                print(f"Error processing {src}: {e}")
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(compress_worker, pdf_tasks)
        print("All PDFs processed (compressed/copied).")

    # Generate CSS
    css_dir = os.path.join(OUTPUT_DIR, "assets", "css")
    ensure_dir(css_dir)
    with open(os.path.join(css_dir, "style.css"), "w", encoding='utf-8') as f:
        f.write(CSS_CONTENT)

    # Core Pages
    core_pages = [("index.md", "Home"), ("biography.md", "Biography")]
    for filename, default_title in core_pages:
        md_path = os.path.join(ROOT_DIR, filename)
        if not os.path.exists(md_path):
            md_path = os.path.join(ROOT_DIR, "documentation", filename)
        if os.path.exists(md_path):
            content, meta = convert_md_to_html(md_path)
            title = meta.get('title', default_title)
            output_path = os.path.join(OUTPUT_DIR, filename.replace('.md', '.html'))
            generate_page(output_path, title, content, depth=0)

    # Articles
    article_links = []
    for xml_path in article_files:
        filename = os.path.basename(xml_path)
        if not filename.startswith("transcription"):
            continue
            
        content, meta = convert_tei_to_html(xml_path)
        title = meta.get('title', os.path.splitext(filename)[0].replace('_', ' ')).strip('"')
        date = meta.get('date', '').strip('"')
        article_id = meta.get('article_id', '').strip('"')
        
        if not article_id:
            continue

        output_filename = filename.replace('.xml', '.html')
        if article_id and not output_filename.startswith(article_id):
            output_filename = f"{article_id}_{output_filename}"

        facsimile_html = ""
        src_dir = os.path.dirname(xml_path)
        pdfs = [f for f in os.listdir(src_dir) if f.lower().endswith(".pdf") and "reject" not in f.lower()]
        if pdfs:
            pdfs.sort()
            pdf_name = pdfs[0]
            facsimile_html = f"""
<div class="facsimile-pane" style="height: 80vh; min-height: 600px; padding: 0;">
    <iframe src="../articles/{pdf_name}" style="width: 100%; height: 100%; border: none; border-radius: 4px;"></iframe>
</div>
"""

        tei_html = ""
        if article_id:
            dest_tei_dir = os.path.join(OUTPUT_DIR, "tei", article_id)
            ensure_dir(dest_tei_dir)
            xml_name = os.path.basename(xml_path)
            safe_copy(xml_path, os.path.join(dest_tei_dir, xml_name))
            tei_html = f'<div style="margin-top: 0.5rem; display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;"><span class="meta" style="margin-right: 0.5rem;">TEI Source:</span><a href="../tei/{article_id}/{xml_name}" target="_blank" class="tei-link">📜 {xml_name}</a></div>'

        meta_html = ""
        if article_id: meta_html += f'<p class="meta">ID: {article_id}</p>'
        if date: meta_html += f'<p class="meta">Date: {date}</p>'
        if tei_html: meta_html += tei_html

        article_content = ARTICLE_TEMPLATE.format(
            title=title, meta_html=meta_html, content=content, facsimile_html=facsimile_html
        )

        output_path = os.path.join(articles_out_dir, output_filename)
        generate_page(output_path, title, article_content, depth=1)

        article_links.append({
            'title': title, 'date': date, 'url': f"articles/{output_filename}", 'id': article_id
        })

    article_links.sort(key=lambda x: (x['id'] or "zzz", x['title']))

    articles_list_html = "<h1>Articles</h1>\n<ul class='article-list'>\n"
    for link in article_links:
        date_span = f" <span class='meta'>({link['date']})</span>" if link['date'] else ""
        articles_list_html += f'<li><a href="{link["url"]}">{link["title"]}</a>{date_span}</li>\n'
    articles_list_html += "</ul>"

    generate_page(os.path.join(OUTPUT_DIR, "articles.html"), "Articles", articles_list_html, depth=0)

    # Generate Books Page
    books_html = "<h1>Books & Editions</h1>\n<ul class='article-list'>\n"
    if bib_data:
        books = sorted([(k, v) for k, v in bib_data.items() if k.startswith("7.b.")])
        for book_id, citation in books:
            display_id = book_id.replace("7.b.", "Book ")
            pdf_name = f"{book_id}.pdf"
            
            dest_pdf_path = os.path.join(OUTPUT_DIR, "books", pdf_name)
            link_html = ""
            if os.path.exists(dest_pdf_path):
                clean_title = citation.split(', ', 1)[0].strip('"').strip('\'')
                if len(clean_title) > 80:
                    clean_title = clean_title[:77] + "..."
                full_display_title = f"{display_id} &mdash; {clean_title}"
                
                book_viewer_content = f"""
<article>
    <div class="edition-container">
        <div class="transcription-pane">
            <header>
                <h1>{display_id}</h1>
                <p class="meta">Bibliography Reference: {book_id}</p>
            </header>
            <div class="content">
                <p>This volume is part of Professor Ernest John Revell's digitized scholarly bibliography corpus. The right pane displays the interactive digitized facsimile scan of the full volume.</p>
                <blockquote style="font-size: 1.1rem; border-left: 4px solid var(--accent-color); margin: 1.5rem 0; padding: 1rem; color: #555; background: #f9f9f9; font-style: italic; border-radius: 4px;">
                    {citation}
                </blockquote>
                <div style="margin-top: 2rem;">
                    <a href="../books/{pdf_name}" download class="tei-link" style="background: #eafaf1; border-color: #c2f0d5; color: #27ae60; padding: 0.5rem 1rem; font-size: 1rem; border-radius: 4px; font-weight: bold; display: inline-block;">💾 Download Complete PDF</a>
                </div>
            </div>
        </div>
        <div class="facsimile-pane" style="height: 80vh; min-height: 600px; padding: 0;">
            <iframe src="../books/{pdf_name}" style="width: 100%; height: 100%; border: none; border-radius: 4px;"></iframe>
        </div>
    </div>
</article>
"""
                generate_page(os.path.join(OUTPUT_DIR, "books", f"{book_id}.html"), full_display_title, book_viewer_content, depth=1)
                link_html = f'<div style="margin-top: 0.5rem;"><a href="books/{book_id}.html" class="tei-link" style="background: #eafaf1; border-color: #c2f0d5; color: #27ae60;">📖 Read Book in Viewer</a></div>'
            
            books_html += f'<li><strong style="color: var(--primary-color); font-family: var(--font-heading); font-size: 1.2rem; display: block;">{display_id}</strong><p style="margin: 0.2rem 0 0 0; color: var(--text-color); font-size: 1rem;">{citation}</p>{link_html}</li>\n'
    else:
        books_html += "<li>No books found in bibliography.</li>\n"
    books_html += "</ul>"
    
    generate_page(os.path.join(OUTPUT_DIR, "books.html"), "Books", books_html, depth=0)
    print("\nSite generation complete!")

if __name__ == "__main__":
    main()
