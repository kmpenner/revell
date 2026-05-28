import fitz
import os

pdf_path = r"g:\My Drive\Research\Revell\07a Articles\07a.14 - Aristotle Accents Journal\07a.14.pdf"
superfluous_dir = r"g:\My Drive\Research\Revell\superfluous"
superfluous_path = os.path.join(superfluous_dir, "07a.14_pages_1-3.pdf")

def main():
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    if not os.path.exists(superfluous_dir):
        os.makedirs(superfluous_dir)

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"Original pages: {total}")

    if total <= 3:
        print("PDF too short to remove 3 pages.")
        doc.close()
        return

    # Keep pages 4 to end (0-indexed 3 to total-1)
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=3, to_page=total-1)

    # Save superfluous pages 1-3 (0-indexed 0 to 2)
    sup_doc = fitz.open()
    sup_doc.insert_pdf(doc, from_page=0, to_page=2)
    sup_doc.save(superfluous_path)
    sup_doc.close()

    temp_path = pdf_path + ".temp"
    new_doc.save(temp_path)
    new_doc.close()
    doc.close()

    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"Removed first 3 pages. New count: {total-3}. Superfluous saved to {superfluous_path}")

if __name__ == "__main__":
    main()
