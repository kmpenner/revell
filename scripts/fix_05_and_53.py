
import fitz
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell\07a Articles"

def remove_pages_05():
    pdf_path = os.path.join(ROOT_DIR, "07a.05 - Studies Palestinian Vocalization", "07a.05.pdf")
    temp_path = pdf_path + ".temp"

    if not os.path.exists(pdf_path):
        print(f"Skipping {pdf_path}: Not found.")
        return

    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"07a.05.pdf current pages: {total}")

    # User wants to remove pages 2 and 54 (1-indexed).
    # In 0-indexed terms, these are 1 and 53.
    # We must be careful: removing 1 first makes 53 become 52.
    # It's safer to keep all pages EXCEPT 1 and 53.

    pages_to_keep = [i for i in range(total) if i not in [1, 53]]

    new_doc = fitz.open()
    new_doc.insert_pdf(doc, select=pages_to_keep)
    new_doc.save(temp_path)
    new_doc.close()
    doc.close()

    os.remove(pdf_path)
    os.rename(temp_path, pdf_path)
    print(f"07a.05.pdf saved. New page count: {len(pages_to_keep)}")

def move_05_md():
    src = os.path.join(ROOT_DIR, "07a.05 - Studies Palestinian Vocalization", "07a.05.md")
    dest_dir = os.path.join(ROOT_DIR, "07a.24 - Battle Benjamin Jud")
    dest = os.path.join(dest_dir, "07a.24_v3.md")

    if os.path.exists(src):
        os.makedirs(dest_dir, exist_ok=True)
        print(f"Moving {src} -> {dest}")
        shutil.move(src, dest)
    else:
        print(f"Source not found: {src}")

def fix_53_folders():
    folder1 = os.path.join(ROOT_DIR, "07a.53 - Midian and Ishmael")
    folder2 = os.path.join(ROOT_DIR, "07a.53 - Midian Ishmael Genesis")

    # Consolidate into "07a.53 - Midian and Ishmael" (which is what I used in fix_misfiled_md.py)
    target = folder1
    source = folder2

    if os.path.exists(source) and os.path.exists(target):
        for item in os.listdir(source):
            src_item = os.path.join(source, item)
            dest_item = os.path.join(target, item)
            if not os.path.exists(dest_item):
                print(f"Moving {item} from {source} to {target}")
                shutil.move(src_item, dest_item)
            else:
                print(f"Conflict: {item} already exists in {target}. Skipping.")

        # If folder2 is now empty, delete it
        if not os.listdir(source):
            print(f"Removing empty folder: {source}")
            os.rmdir(source)

if __name__ == "__main__":
    remove_pages_05()
    move_05_md()
    fix_53_folders()
