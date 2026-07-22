import xml.etree.ElementTree as ET
import re

xml_path = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a Articles/07a.04 - New Biblical Fragment/transcription_tei.xml"

with open(xml_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Let's find all '<note' and '<ptr' tags by scanning lines
for idx, line in enumerate(lines):
    line_num = idx + 1
    if '<note' in line:
        # Find matches of <note ...>
        matches = re.finditer(r'<note([^>]*)>', line)
        for m in matches:
            attrs = m.group(1)
            # Find the closing tag or end of line
            snippet = line[m.start():m.start()+150]
            print(f"Line {line_num}: NOTE attrs='{attrs}' | snippet: {snippet.strip()}")
    if '<ptr' in line:
        matches = re.finditer(r'<ptr([^>]*)>', line)
        for m in matches:
            attrs = m.group(1)
            snippet = line[m.start():m.start()+150]
            print(f"Line {line_num}: PTR attrs='{attrs}' | snippet: {snippet.strip()}")
