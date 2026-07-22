import sys
import os
import webbrowser

# Add scripts directory to path to import generate_site
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import generate_site

def preview_xml(xml_path):
    if not os.path.exists(xml_path):
        print(f"Error: File '{xml_path}' not found.")
        sys.exit(1)

    # 1. Parse TEI XML using the site's HTMLParser
    print("Parsing TEI XML...")
    content, meta = generate_site.convert_tei_to_html(xml_path)
    title = meta.get('title', 'TEI Preview')
    article_id = meta.get('article_id', '')
    date = meta.get('date', '')

    # 2. Check for matching PDF facsimile in the source folder
    facsimile_html = ""
    src_dir = os.path.dirname(os.path.abspath(xml_path))
    pdfs = [f for f in os.listdir(src_dir) if f.lower().endswith(".pdf") and "reject" not in f.lower()]
    if pdfs:
        pdfs.sort()
        pdf_abs_path = os.path.abspath(os.path.join(src_dir, pdfs[0]))
        facsimile_html = f"""
        <div class="facsimile-pane" style="height: 80vh; min-height: 600px; padding: 0;">
            <iframe src="file:///{pdf_abs_path.replace(os.sep, '/')}" style="width: 100%; height: 100%; border: none; border-radius: 4px;"></iframe>
        </div>
        """

    # 3. Format page elements
    meta_html = ""
    if article_id: meta_html += f'<p class="meta">ID: {article_id}</p>'
    if date: meta_html += f'<p class="meta">Date: {date}</p>'

    article_content = generate_site.ARTICLE_TEMPLATE.format(
        title=title, meta_html=meta_html, content=content, facsimile_html=facsimile_html
    )

    # 4. Generate standalone preview HTML page
    preview_output = os.path.join(generate_site.OUTPUT_DIR, "preview.html")
    generate_site.ensure_dir(generate_site.OUTPUT_DIR)
    
    # Ensure style.css is generated
    css_dir = os.path.join(generate_site.OUTPUT_DIR, "assets", "css")
    generate_site.ensure_dir(css_dir)
    with open(os.path.join(css_dir, "style.css"), "w", encoding='utf-8') as f:
        f.write(generate_site.CSS_CONTENT)

    generate_site.generate_page(preview_output, title, article_content, depth=0)
    
    # 5. Open in browser
    preview_url = f"file:///{os.path.abspath(preview_output).replace(os.sep, '/')}"
    print(f"\nSuccess! Preview generated at: {preview_output}")
    print("Opening preview in your browser...")
    webbrowser.open(preview_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python preview_tei.py <path_to_xml>")
        sys.exit(1)
    preview_xml(sys.argv[1])
