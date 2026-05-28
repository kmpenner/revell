
import fitz
import os

pdf_path = r"g:\My Drive\Research\Revell\07a Articles\07a.01 - Order Elements Verbal\07a.01.pdf"
temp_path = r"g:\My Drive\Research\Revell\07a Articles\07a.01 - Order Elements Verbal\07a.01_temp.pdf"

def main():
    if not os.path.exists(pdf_path):
        print("PDF not found.")
        return

    doc = fitz.open(pdf_path)
    print(f"Original Page Count: {len(doc)}")

    # Create new doc from first 12 pages (0-indexed 0 to 11)
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=0, to_page=11)
    new_doc.save(temp_path)
    new_doc.close()
    doc.close()

    # Replace old with new
    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print("PDF split successfully. Kept pages 1-12.")

if __name__ == "__main__":
    main()
