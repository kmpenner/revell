
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
MISFILED_DIR = os.path.join(ROOT_DIR, "misfiled")
BACKUPS_DIR = os.path.join(ROOT_DIR, "backups")

def move_pdf(src_path, target_id):
    if not os.path.exists(src_path):
        print(f"Source not found: {src_path}")
        return

    # Find target folder
    target_folder = None
    for f in os.listdir(ARTICLES_DIR):
        if f.startswith(target_id) and os.path.isdir(os.path.join(ARTICLES_DIR, f)):
            target_folder = f
            break

    if target_folder:
        dest_dir = os.path.join(ARTICLES_DIR, target_folder)
        # Check for existing PDFs to avoid overwrite, though we want clean names
        existing = [f for f in os.listdir(dest_dir) if f.lower().endswith(".pdf")]
        if not existing:
            new_name = f"{target_id}.pdf"
        else:
            new_name = f"{target_id}_v{len(existing)+1}.pdf"

        dest_path = os.path.join(dest_dir, new_name)
        print(f"Moving {os.path.basename(src_path)} -> {target_folder}/{new_name}")
        shutil.move(src_path, dest_path)
    else:
        print(f"Target folder for {target_id} not found.")

def main():
    # Based on Audit Results

    # 7.a.47 "The Reading Tradition" was found in:
    moves = [
        (os.path.join(ARTICLES_DIR, "07a.37 - Conjunctive Dagesh Preliminary", "07a.37_p1.pdf"), "07a.47"),
        (os.path.join(ARTICLES_DIR, "07a.38 - Dehiq Exceptions Masoretic", "07a.38_p1.pdf"), "07a.47"),
        (os.path.join(ARTICLES_DIR, "07a.38 - Dehiq Exceptions Masoretic", "07a.38_p2.pdf"), "07a.47"),
        (os.path.join(ARTICLES_DIR, "07a.40 - First Person Imperfect", "07a.40_p1.pdf"), "07a.47"),
        (os.path.join(ARTICLES_DIR, "07a.40 - First Person Imperfect", "07a.40_p2.pdf"), "07a.47"),
        (os.path.join(ARTICLES_DIR, "07a.41 - Language Interpretation 1", "07a.41_p2.pdf"), "07a.47"),
    ]

    # 7.a.12 "Saadya Gaon" found in:
    moves.append((os.path.join(MISFILED_DIR, "07a.08_reprint_cover.pdf"), "07a.12"))
    moves.append((os.path.join(BACKUPS_DIR, "07a.08_The_Oldest_Accent_List_in_the_Diqduqe_ha-Te'amim.pdf"), "07a.12"))

    # 7.a.20 "Pausal Forms Poetry" found in:
    moves.append((os.path.join(BACKUPS_DIR, "07a.30_The_Conditioning_of_Stress_Position_in_Waw_Consecutive_Perfect_Forms_in_Biblical_Hebrew.pdf"), "07a.20"))

    # 7.a.28 "Pausal Phenomenon Palestinian" found in:
    moves.append((os.path.join(MISFILED_DIR, "07a.XX_System_of_the_Finite_Verb.pdf"), "07a.28"))

    # Execute moves
    for src, tid in moves:
        move_pdf(src, tid)

if __name__ == "__main__":
    main()
