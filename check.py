import os
import fitz

pdf_path = r"c:\Users\kpenner\Google Drive\Research\Revell\07a Articles\07a.04 - New Biblical Fragment\07a.04.pdf"
doc = fitz.open(pdf_path)
print("PDF Pages:", len(doc))
for i in range(len(doc)):
    page = doc.load_page(i)
    print(f"Page {i+1} rect:", page.rect)
doc.close()
