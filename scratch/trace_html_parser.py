import sys
import os
sys.path.append("/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/scripts")
import generate_site

temp_xml = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/scratch/temp_test.xml"
with open(temp_xml, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>Test</title></titleStmt><publicationStmt><p>Test</p></publicationStmt><sourceDesc><p>Test</p></sourceDesc></fileDesc></teiHeader><text><body><fw type="header" place="top">E. J. REVELL</fw></body></text></TEI>')

html, meta = generate_site.convert_tei_to_html(temp_xml)
print("Output HTML:", repr(html))
