import sys
import os

sys.path.append("/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/scripts")
import generate_site

xml_path = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/docs/tei/07a.02/transcription_tei.xml"
if os.path.exists(xml_path):
    html, meta = generate_site.convert_tei_to_html(xml_path)
    # Print lines containing E. J. REVELL
    lines = html.split("\n")
    for idx, line in enumerate(lines):
        if "REVELL" in line:
            print(f"Line {idx+1}: {line}")
else:
    print("XML path not found")
