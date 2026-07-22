import sys
sys.path.append("/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/scripts")
import generate_site

xml_path = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/docs/tei/07a.02/transcription_tei.xml"
html, meta = generate_site.convert_tei_to_html(xml_path)

# Let's find '<fw' in html
import re
for m in re.finditer(r'<fw[^>]*>', html):
    start = max(0, m.start() - 100)
    end = min(len(html), m.end() + 100)
    print(f"Match at position {m.start()}:")
    print(html[start:end])
    print("-" * 50)
