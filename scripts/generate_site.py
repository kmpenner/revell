
import os
import markdown
import shutil
import glob
import re
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.exists(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "07a Articles")) else r"g:\My Drive\Research\Revell"
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

<script>
function changePage(delta, totalPages) {{
    const img = document.getElementById('facsimile-img');
    const pageNumEl = document.getElementById('page-number');
    let currentPage = parseInt(pageNumEl.innerText);
    let newPage = currentPage + delta;

    if (newPage >= 1 && newPage <= totalPages) {{
        pageNumEl.innerText = newPage;
        // Construct new image path
        const currentSrc = img.src;
        img.src = currentSrc.substring(0, currentSrc.lastIndexOf('/') + 1) + 'page_' + newPage + '.png';
    }}
}}
</script>
"""

FACSIMILE_TEMPLATE = """
<div class="facsimile-pane">
    <div class="facsimile-controls">
        <button onclick="changePage(-1, {total_pages})">&laquo; Previous</button>
        <span>Page <span id="page-number">1</span> of {total_pages}</span>
        <button onclick="changePage(1, {total_pages})">Next &raquo;</button>
    </div>
    <img id="facsimile-img" src="{first_page_url}" alt="Page 1 facsimile">
</div>
"""

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def compress_pdf(src_path, dest_path):
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
    
    shutil.copy2(src_path, dest_path)
    return False

def fix_links(html_content):
    # Regex to replace .md links with .html
    # Matches href="something.md"
    return re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html_content)

def convert_md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    md = markdown.Markdown(extensions=['meta', 'fenced_code', 'tables'])
    html_content = md.convert(text)

    # Fix links in the content
    html_content = fix_links(html_content)

    meta = md.Meta if hasattr(md, 'Meta') else {}
    flattened_meta = {k: v[0] if isinstance(v, list) and v else "" for k, v in meta.items()}

    return html_content, flattened_meta

def generate_page(output_path, title, content, depth=0):
    root_path = "../" * depth if depth > 0 else ""
    css_path = f"{root_path}assets/css/style.css"

    # Fix links in the full page content as well (just in case)
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
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    ensure_dir(OUTPUT_DIR)

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
    article_files = glob.glob(os.path.join(ARTICLES_DIR, "**/*.md"), recursive=True)

    articles_out_dir = os.path.join(OUTPUT_DIR, "articles")
    ensure_dir(articles_out_dir)

    for md_path in article_files:
        filename = os.path.basename(md_path)
        
        # Filter out extraneous non-article files
        if not filename.startswith("07a."):
            continue
        if "reject" in filename.lower() or "checklist" in filename.lower() or "transcription" in filename.lower():
            continue
        if "reviews" in md_path.lower() or "rescan" in md_path.lower() or "to do" in md_path.lower():
            continue
            
        output_filename = filename.replace('.md', '.html')
        content, meta = convert_md_to_html(md_path)
        title = meta.get('title', os.path.splitext(filename)[0].replace('_', ' ')).strip('"')
        date = meta.get('date', '').strip('"')
        article_id = meta.get('article_id', '').strip('"')
        
        if not article_id:
            continue

        # Facsimile Handling
        facsimile_html = ""
        src_dir = os.path.dirname(md_path)
        # Find any PDF in this directory (ignoring "reject" in name)
        pdfs = [f for f in os.listdir(src_dir) if f.lower().endswith(".pdf") and "reject" not in f.lower()]
        if pdfs:
            pdfs.sort()
            pdf_name = pdfs[0]
            # Compress and copy PDF to docs/articles/
            dest_pdf_path = os.path.join(articles_out_dir, pdf_name)
            compress_pdf(os.path.join(src_dir, pdf_name), dest_pdf_path)
            
            # Render embedded PDF reader
            facsimile_html = f"""
<div class="facsimile-pane" style="height: 80vh; min-height: 600px; padding: 0;">
    <iframe src="../articles/{pdf_name}" style="width: 100%; height: 100%; border: none; border-radius: 4px;"></iframe>
</div>
"""

        # Copy and link TEI XML source files
        tei_html = ""
        src_dir = os.path.dirname(md_path)
        xml_files = sorted(glob.glob(os.path.join(src_dir, "*.xml")))
        if xml_files:
            dest_tei_dir = os.path.join(OUTPUT_DIR, "tei", article_id)
            ensure_dir(dest_tei_dir)
            
            tei_links = []
            for xml_path in xml_files:
                xml_name = os.path.basename(xml_path)
                shutil.copy2(xml_path, os.path.join(dest_tei_dir, xml_name))
                tei_links.append(f'<a href="../tei/{article_id}/{xml_name}" target="_blank" class="tei-link">📜 {xml_name}</a>')
                
            tei_html = '<div style="margin-top: 0.5rem; display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;"><span class="meta" style="margin-right: 0.5rem;">TEI Source:</span>' + ''.join(tei_links) + '</div>'

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
    bib_path = os.path.join(ROOT_DIR, "metadata", "bibliography.json")
    if os.path.exists(bib_path):
        import json
        with open(bib_path, 'r', encoding='utf-8') as f:
            bib_data = json.load(f)
        
        books_out_dir = os.path.join(OUTPUT_DIR, "books")
        ensure_dir(books_out_dir)
        
        books = sorted([(k, v) for k, v in bib_data.items() if k.startswith("7.b.")])
        for book_id, citation in books:
            # Clean and present book citation beautifully
            display_id = book_id.replace("7.b.", "Book ")
            
            # Find matching PDF files for this book
            book_num = int(book_id.split(".")[-1])
            pdf_path = None
            pdf_name = f"{book_id}.pdf"
            
            books_src_dir = os.path.join(ROOT_DIR, "07b Books")
            if os.path.exists(books_src_dir):
                for root, dirs, files in os.walk(books_src_dir):
                    for file in files:
                        if file.lower().endswith(".pdf"):
                            parent_folder = os.path.basename(root)
                            if (parent_folder.startswith(f"07b.{book_num}") or 
                                file.startswith(f"07b.{book_num}") or 
                                file.startswith(f"7.b.{book_num}") or 
                                file.startswith(f"Revell 07b.{book_num}")):
                                pdf_path = os.path.join(root, file)
                                break
                    if pdf_path:
                        break
            
            link_html = ""
            if pdf_path and os.path.exists(pdf_path):
                dest_pdf_path = os.path.join(books_out_dir, pdf_name)
                compress_pdf(pdf_path, dest_pdf_path)
                
                # Generate a dedicated book viewer page
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
                generate_page(os.path.join(books_out_dir, f"{book_id}.html"), full_display_title, book_viewer_content, depth=1)
                
                link_html = f'<div style="margin-top: 0.5rem;"><a href="books/{book_id}.html" class="tei-link" style="background: #eafaf1; border-color: #c2f0d5; color: #27ae60;">📖 Read Book in Viewer</a></div>'
            
            books_html += f'<li><strong style="color: var(--primary-color); font-family: var(--font-heading); font-size: 1.2rem; display: block;">{display_id}</strong><p style="margin: 0.2rem 0 0 0; color: var(--text-color); font-size: 1rem;">{citation}</p>{link_html}</li>\n'
    else:
        books_html += "<li>No books found in bibliography.</li>\n"
    books_html += "</ul>"
    
    generate_page(os.path.join(OUTPUT_DIR, "books.html"), "Books", books_html, depth=0)
    print("\nSite generation complete!")

if __name__ == "__main__":
    main()
