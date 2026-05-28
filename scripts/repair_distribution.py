
import os
import shutil
import fitz

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")

def merge_pdfs(pdf_list, output_path):
    result = fitz.open()
    for pdf in pdf_list:
        with fitz.open(pdf) as mfile:
            result.insert_pdf(mfile)
    result.save(output_path)
    result.close()

def main():
    # 1. Repatriation (based on deep_audit_results.txt)
    # Target structure: folder ID mapping

    # 07a.01/part2 -> 07a.04
    # 07a.30/part3 -> 07b.05 (create folder or move to 07b)
    # 07a.41/part1 -> 07a.01
    # 07a.44/part2 -> 07a.48

    # Let's do this safely
    moves = [
        (os.path.join(ARTICLES_DIR, "07a.01 - The Order of the Elements in the Verbal Statement Clause in 1Q Serek", "07a.01_The_Order_of_the_Elements_in_the_Verbal_Statement_Clause_in_1Q_Serek_part2.pdf"), "07a.04"),
        (os.path.join(ARTICLES_DIR, "07a.24 - The Battle with Benjamin (Jud. XX 29-48) and Hebrew Narrative Techniques", "07a.24_The_Battle_with_Benjamin_(Jud._XX_29-48)_and_Hebrew_Narrative_Techniques_part1.pdf"), "07a.24"), # Wait, Jud. XX 29-48 is 7.a.24. So part1 and part2 are BOTH 7.a.24.
        (os.path.join(ARTICLES_DIR, "07a.30 - The Conditioning of Stress Position in Waw Consecutive Perfect Forms in Biblical Hebrew", "07a.30_The_Conditioning_of_Stress_Position_in_Waw_Consecutive_Perfect_Forms_in_Biblical_Hebrew_part3.pdf"), "07b.05"), # Special case
        (os.path.join(ARTICLES_DIR, "07a.41 - Language and Interpretation in 1 Kings 20", "07a.41_Language_and_Interpretation_in_1_Kings_20_part1.pdf"), "07a.01"),
        (os.path.join(ARTICLES_DIR, "07a.44 - Concord with Collectives in Biblical Narrative", "07a.44_Concord_with_Collectives_in_Biblical_Narrative_part2.pdf"), "07a.48")
    ]

    # Note: 07a.24 part1 and part2 are both 24, so they should be merged.

    print("--- REPATRIATING MISIDENTIFIED FILES ---")
    for src, target_id in moves:
        if not os.path.exists(src):
            continue

        # Find target folder
        target_folder = None
        for f in os.listdir(ARTICLES_DIR):
            if f.startswith(target_id):
                target_folder = f
                break

        if target_folder:
            dest_dir = os.path.join(ARTICLES_DIR, target_folder)
            print(f"Moving {os.path.basename(src)} to {target_folder}")
            shutil.move(src, os.path.join(dest_dir, os.path.basename(src)))
        elif target_id == "07b.05":
            # Move to 07b Books if exists
            books_dir = os.path.join(ROOT_DIR, "07b Books")
            if os.path.exists(books_dir):
                 print(f"Moving {os.path.basename(src)} to 07b Books")
                 shutil.move(src, os.path.join(books_dir, os.path.basename(src)))

    print("\n--- MERGING MULTI-PART ARTICLES ---")
    # For each folder with > 1 PDF, merge them in order.
    for folder in os.listdir(ARTICLES_DIR):
        folder_path = os.path.join(ARTICLES_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        pdfs = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])
        if len(pdfs) > 1:
            print(f"Merging {len(pdfs)} PDFs in {folder}...")
            # Detect sanitized name from folder
            if " - " in folder:
                parts = folder.split(" - ", 1)
                base_name = f"{parts[0]}_{parts[1].replace(' ', '_').replace(':', '').replace('/', '')}"
            else:
                base_name = folder.replace(' ', '_')

            if len(base_name) > 100: base_name = base_name[:100]

            output_name = f"{base_name}.pdf"
            output_path = os.path.join(folder_path, output_name)

            full_paths = [os.path.join(folder_path, p) for p in pdfs]
            merge_pdfs(full_paths, output_path)

            print(f"  Created {output_name}. Clean up old parts...")
            for p in full_paths:
                if os.path.abspath(p) != os.path.abspath(output_path):
                    os.remove(p)

if __name__ == "__main__":
    main()
