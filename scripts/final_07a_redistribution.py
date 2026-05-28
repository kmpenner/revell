
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
FOLDER_47 = os.path.join(ARTICLES_DIR, "07a.47 - Reading Tradition Basis")

def move_to_id(src_filename, target_id):
    src_path = os.path.join(FOLDER_47, src_filename)
    if not os.path.exists(src_path):
        return

    # Find target folder
    target_folder = None
    for f in os.listdir(ARTICLES_DIR):
        if f.startswith(target_id) and os.path.isdir(os.path.join(ARTICLES_DIR, f)):
            target_folder = f
            break

    if target_folder:
        dest_dir = os.path.join(ARTICLES_DIR, target_folder)
        existing = [f for f in os.listdir(dest_dir) if f.lower().endswith(".pdf")]
        if not existing:
            new_name = f"{target_id}.pdf"
        else:
            new_name = f"{target_id}_v{len(existing)+1}.pdf"

        dest_path = os.path.join(dest_dir, new_name)
        print(f"Moving {src_filename} -> {target_folder}/{new_name}")
        shutil.move(src_path, dest_path)
    else:
         print(f"Target folder for {target_id} not found.")

def main():
    # Final redistribution from 07a.47
    # v6 -> 07a.41
    move_to_id("07a.47_v6.pdf", "07a.41")
    # v5 -> 07a.40
    move_to_id("07a.47_v5.pdf", "07a.40")
    # v4 -> 07a.40 (probably more of 40)
    move_to_id("07a.47_v4.pdf", "07a.40")
    # v3 -> 07a.38
    move_to_id("07a.47_v3.pdf", "07a.38")
    # v2 -> 07a.38 (Likely the context/rest of it)
    move_to_id("07a.47_v2.pdf", "07a.38")

    # Cleanup 07a.47 (Keep only the 18-page one if it's correct)
    # Actually, I'll just rename v1 to 07a.47.pdf if it's there, but I have 07a.47.pdf already.

if __name__ == "__main__":
    main()
