import xml.etree.ElementTree as ET

xml_path = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a Articles/07a.04 - New Biblical Fragment/transcription_tei.xml"

with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the unclosed <p> tag on line 670
content = content.replace(
    "<p>It is therefore entirely reasonable to suppose that the\n\n            \n            <pb n=\"71\" />",
    "<p>It is therefore entirely reasonable to suppose that the</p>\n\n            \n            <pb n=\"71\" />"
)

try:
    ET.fromstring(content)
    print("Success! The XML is now well-formed.")
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(content)
except Exception as e:
    print(f"Error parsing: {e}")
    # Let's inspect content around the error
    match = re.search(r'line (\d+)', str(e))
    if match:
        line_num = int(match.group(1))
        lines = content.split('\n')
        for i in range(max(0, line_num - 10), min(len(lines), line_num + 10)):
            print(f"{i+1}: {lines[i]}")
