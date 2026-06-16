import fitz
import os

ROOT_DIR = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a Articles"
SUPERFLUOUS_DIR = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/superfluous"

def split_07a_31():
    pdf_path = os.path.join(ROOT_DIR, "07a.31 - Stress Position Hebrew", "07a.31.pdf")
    temp_path = pdf_path + ".temp"

    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    if not os.path.exists(SUPERFLUOUS_DIR):
        os.makedirs(SUPERFLUOUS_DIR)

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"07a.31.pdf current pages: {total}")

    if total < 2:
        print("Error: PDF has only 1 page. Cannot remove page 1.")
        doc.close()
        return

    # Keep page 2 to the end (0-indexed: 1 to total-1)
    main_doc = fitz.open()
    main_doc.insert_pdf(doc, from_page=1, to_page=total-1)
    main_doc.save(temp_path)
    main_doc.close()

    # Move page 1 (0-indexed: 0) to superfluous
    out_doc = fitz.open()
    out_doc.insert_pdf(doc, from_page=0, to_page=0)
    out_path = os.path.join(SUPERFLUOUS_DIR, "07a.31_page_1.pdf")
    out_doc.save(out_path)
    out_doc.close()

    doc.close()

    # Replace old with new
    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"07a.31.pdf split successfully. Kept pages 2-{total} (now 1-{total-1}).")
    print(f"Page 1 moved to {out_path}")

if __name__ == "__main__":
    split_07a_31()
