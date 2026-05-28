import fitz
import os

pdf_path = r"g:\My Drive\Research\Revell\07a Articles\07a.15 - Diacritical Dots Development\07a.15.pdf"
superfluous_dir = r"g:\My Drive\Research\Revell\superfluous"
superfluous_start = os.path.join(superfluous_dir, "07a.15_start.pdf")
superfluous_end = os.path.join(superfluous_dir, "07a.15_end.pdf")

def main():
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    if not os.path.exists(superfluous_dir):
        os.makedirs(superfluous_dir)

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"Original pages: {total}")

    # Keep pages 5-7. 1-indexed. So 0-indexed: 4, 5, 6
    # Keep slice [4:7]
    range_start = 4 # 5th page
    range_end = 6   # 7th page (inclusive)

    if total <= range_start:
        print("PDF too short to apply range.")
        doc.close()
        return

    # Check boundaries
    effective_range_end = min(range_end, total - 1)

    # New document with kept pages
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=range_start, to_page=effective_range_end)

    # Save superfluous parts
    # Part 1: Pages 1-4 (0-3)
    if range_start > 0:
        sup_doc1 = fitz.open()
        sup_doc1.insert_pdf(doc, from_page=0, to_page=range_start-1)
        sup_doc1.save(superfluous_start)
        sup_doc1.close()
        print(f"Saved superfluous start to {superfluous_start}")

    # Part 2: Pages 8-end (7-end)
    if effective_range_end < total - 1:
        sup_doc2 = fitz.open()
        sup_doc2.insert_pdf(doc, from_page=effective_range_end+1, to_page=total-1)
        sup_doc2.save(superfluous_end)
        sup_doc2.close()
        print(f"Saved superfluous end to {superfluous_end}")

    temp_path = pdf_path + ".temp"
    new_doc.save(temp_path)
    new_doc.close()
    doc.close()

    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"Kept pages {range_start+1}-{effective_range_end+1}. New count: {len(new_doc)}")

if __name__ == "__main__":
    main()
