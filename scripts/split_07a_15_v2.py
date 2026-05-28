import fitz
import os

pdf_path = r"g:\My Drive\Research\Revell\07a Articles\07a.15 - Diacritical Dots Development\07a.15.pdf"
superfluous_dir = r"g:\My Drive\Research\Revell\superfluous"

# Create dir if not exists
if not os.path.exists(superfluous_dir):
    os.makedirs(superfluous_dir)

def split_pdf():
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    # Open source
    src = fitz.open(pdf_path)
    total = len(src)
    print(f"Total pages: {total}")

    # Desired: Pages 5-7 (0-indexed 4, 5, 6)
    keep_start = 4
    keep_end = 6 # inclusive

    # 1. Main file (pages 5-7)
    doc_main = fitz.open()
    doc_main.insert_pdf(src, from_page=keep_start, to_page=keep_end)
    temp_main = pdf_path.replace(".pdf", "_temp.pdf")
    doc_main.save(temp_main)
    doc_main.close()
    print(f"saved main content to {temp_main}")

    # 2. Superfluous Start (Pages 1-4 -> 0-3)
    # 0-indexed: 0 to keep_start-1
    if keep_start > 0:
        doc_sup1 = fitz.open()
        doc_sup1.insert_pdf(src, from_page=0, to_page=keep_start-1)
        sup1_path = os.path.join(superfluous_dir, "07a.15_pages_1-4.pdf")
        doc_sup1.save(sup1_path)
        doc_sup1.close()
        print(f"saved superfluous start to {sup1_path}")

    # 3. Superfluous End (Pages 8-end -> 7 to total-1)
    # 0-indexed: keep_end+1 to total-1
    if keep_end < total - 1:
        doc_sup2 = fitz.open()
        doc_sup2.insert_pdf(src, from_page=keep_end+1, to_page=total-1)
        sup2_path = os.path.join(superfluous_dir, "07a.15_pages_8-end.pdf")
        doc_sup2.save(sup2_path)
        doc_sup2.close()
        print(f"saved superfluous end to {sup2_path}")

    src.close()

    # Replace original
    os.remove(pdf_path)
    os.rename(temp_main, pdf_path)
    print("Done.")

if __name__ == "__main__":
    split_pdf()
