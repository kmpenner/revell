
import fitz
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell\07a Articles"
SUPERFLUOUS_DIR = r"g:\My Drive\Research\Revell\superfluous"

def split_07a_09():
    pdf_path = os.path.join(ROOT_DIR, "07a.09 - Grammar Jacob Edessa", "07a.09.pdf")
    temp_path = pdf_path + ".temp"

    if not os.path.exists(pdf_path):
        print(f"Skipping 07a.09 split: {pdf_path} not found.")
        return

    if not os.path.exists(SUPERFLUOUS_DIR):
        os.makedirs(SUPERFLUOUS_DIR)

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"07a.09.pdf current pages: {total}")

    # User wants to keep pages 4-11 (1-indexed).
    # In 0-indexed: 3 to 10.

    if total < 11:
        print(f"Error: 07a.09.pdf only has {total} pages. Cannot keep up to 11.")
        # If it's shorter, maybe the user means different pages?
        # But I'll stick to the request and warn.
        doc.close()
        return

    # Keep pages 4-11
    main_doc = fitz.open()
    # 0-indexed: 3, 4, 5, 6, 7, 8, 9, 10 (8 pages total)
    main_doc.insert_pdf(doc, from_page=3, to_page=10)
    main_doc.save(temp_path)
    main_doc.close()

    # Move others to superfluous (pages 1-3 and 12-end)
    out_doc = fitz.open()
    if 3 > 0:
        out_doc.insert_pdf(doc, from_page=0, to_page=2)
    if total > 11:
        out_doc.insert_pdf(doc, from_page=11, to_page=total-1)

    out_path = os.path.join(SUPERFLUOUS_DIR, "07a.09_superfluous.pdf")
    out_doc.save(out_path)
    out_doc.close()

    doc.close()

    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"07a.09.pdf split. Kept pages 4-11. Superfluous pages moved to {out_path}")

if __name__ == "__main__":
    split_07a_09()
