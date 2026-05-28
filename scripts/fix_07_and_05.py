
import fitz
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell\07a Articles"
SUPERFLUOUS_DIR = r"g:\My Drive\Research\Revell\superfluous"

def split_07a_07():
    pdf_path = os.path.join(ROOT_DIR, "07a.07 - Oldest Evidence Hebrew", "07a.07.pdf")
    temp_path = pdf_path + ".temp"

    if not os.path.exists(pdf_path):
        print(f"Skipping 07a.07 split: {pdf_path} not found.")
        return

    if not os.path.exists(SUPERFLUOUS_DIR):
        os.makedirs(SUPERFLUOUS_DIR)

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"07a.07.pdf current pages: {total}")

    # User wants to keep pages 6-12 (1-indexed).
    # In 0-indexed: 5 to 11.

    if total < 12:
        print(f"Error: 07a.07.pdf only has {total} pages. Cannot keep up to 12.")
        doc.close()
        return

    # Keep pages 6-12
    main_doc = fitz.open()
    # select is 0-indexed. 5, 6, 7, 8, 9, 10, 11
    main_doc.insert_pdf(doc, from_page=5, to_page=11)
    main_doc.save(temp_path)
    main_doc.close()

    # Move others to superfluous (pages 1-5 and 13-end)
    out_doc = fitz.open()
    if 5 > 0:
        out_doc.insert_pdf(doc, from_page=0, to_page=4)
    if total > 12:
        out_doc.insert_pdf(doc, from_page=12, to_page=total-1)

    out_path = os.path.join(SUPERFLUOUS_DIR, "07a.07_superfluous.pdf")
    out_doc.save(out_path)
    out_doc.close()

    doc.close()

    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"07a.07.pdf split. Kept pages 6-12. Superfluous pages moved to {out_path}")

def fix_05_pdf():
    # Attempt 2 for 07a.05 page removal
    pdf_path = os.path.join(ROOT_DIR, "07a.05 - Studies Palestinian Vocalization", "07a.05.pdf")
    temp_path = pdf_path + ".temp"

    if not os.path.exists(pdf_path):
        print(f"Skipping 05 split: {pdf_path} not found.")
        return

    doc = fitz.open(pdf_path)
    total = len(doc)

    # 1-indexed 2 and 54 are 0-indexed 1 and 53.
    # Use select() which is correct for keeping specific pages
    keep_indices = [i for i in range(total) if i not in [1, 53]]

    doc.select(keep_indices)
    doc.save(temp_path)
    doc.close()

    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"07a.05.pdf cleaned. Pages 2 and 54 removed.")

if __name__ == "__main__":
    split_07a_07()
    fix_05_pdf()
