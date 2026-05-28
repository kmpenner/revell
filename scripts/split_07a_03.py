
import fitz
import os

pdf_path = r"g:\My Drive\Research\Revell\07a Articles\07a.03 - Sign Sound Study\07a.03.pdf"
temp_main = r"g:\My Drive\Research\Revell\07a Articles\07a.03 - Sign Sound Study\07a.03_temp.pdf"
superfluous_dir = r"g:\My Drive\Research\Revell\superfluous"
superfluous_page = os.path.join(superfluous_dir, "07a.03_last_page.pdf")

def main():
    if not os.path.exists(pdf_path):
        print("PDF not found.")
        return

    if not os.path.exists(superfluous_dir):
        os.makedirs(superfluous_dir)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Original Page Count: {total_pages}")

    if total_pages < 2:
        print("PDF has only one page, cannot split last page.")
        doc.close()
        return

    # Save main article (all pages except last)
    main_doc = fitz.open()
    main_doc.insert_pdf(doc, from_page=0, to_page=total_pages-2)
    main_doc.save(temp_main)
    main_doc.close()

    # Save last page
    last_doc = fitz.open()
    last_doc.insert_pdf(doc, from_page=total_pages-1, to_page=total_pages-1)
    last_doc.save(superfluous_page)
    last_doc.close()

    doc.close()

    # Replace old with new
    os.remove(pdf_path)
    os.rename(temp_main, pdf_path)
    print(f"PDF split successfully. Article kept {total_pages-1} pages. Last page moved to {superfluous_page}")

if __name__ == "__main__":
    main()
