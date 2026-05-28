
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell\07a Articles"

def move_file(rel_src, rel_dest):
    src = os.path.join(ROOT_DIR, rel_src)
    dest = os.path.join(ROOT_DIR, rel_dest)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        print(f"Moving {rel_src} -> {rel_dest}")
        shutil.move(src, dest)
    else:
        print(f"Source not found: {rel_src}")

def main():
    # 1. 07a.05.md -> 07a.24 folder
    move_file(r"07a.05 - Studies Palestinian Vocalization\07a.05.md", r"07a.24 - Battle Benjamin Jud\07a.24_v3.md")

    # 2. 07a.08_p2.md -> 07a.23 folder
    move_file(r"07a.08 - Oldest Accent List\07a.08_p2.md", r"07a.23 - Nesigah History Masorah\07a.23.md")

    # 3. Rename SBH files to descriptive names
    move_file(r"SBH-C368-NT26021315520.pdf", r"reviews\Review_Meier_Speaking_of_Speaking_JAOS_1994.pdf")
    move_file(r"SBH-C368-NT26021315520_ocr.md", r"reviews\Review_Meier_Speaking_of_Speaking_JAOS_1994_ocr.md")

    move_file(r"SBH-C368-NT26021315410.pdf", r"reviews\Review_Fernandez-Tejero_Tradicion_Textual_JBL_1978.pdf")
    move_file(r"SBH-C368-NT26021315410_ocr.md", r"reviews\Review_Fernandez-Tejero_Tradicion_Textual_JBL_1978_ocr.md")

    move_file(r"SBH-C368-NT26021315380.pdf", r"reviews\Review_Kogut_Biblical_Accentuation_HebrewStudies_1997.pdf")
    move_file(r"SBH-C368-NT26021315380_ocr.md", r"reviews\Review_Kogut_Biblical_Accentuation_HebrewStudies_1997_ocr.md")

if __name__ == "__main__":
    main()
