
import os
import shutil

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
MISFILED_DIR = os.path.join(ROOT_DIR, "misfiled")

def main():
    os.makedirs(MISFILED_DIR, exist_ok=True)

    # 07a.08: Remove 07a.08.pdf (it's a reprint cover), keep the other
    path_08 = os.path.join(ARTICLES_DIR, "07a.08 - The Oldest Accent List in the Diqduqe ha-Te'amim", "07a.08.pdf")
    if os.path.exists(path_08):
        shutil.move(path_08, os.path.join(MISFILED_DIR, "07a.08_reprint_cover.pdf"))

    # 07a.24: Move 07a.24.pdf (Function of Clauses) to misfiled
    path_24 = os.path.join(ARTICLES_DIR, "07a.24 - The Battle with Benjamin (Jud. XX 29-48) and Hebrew Narrative Techniques", "07a.24.pdf")
    if os.path.exists(path_24):
        shutil.move(path_24, os.path.join(MISFILED_DIR, "07a.XX_Function_of_Clauses_in_Judges.pdf"))

    # 07a.36: 07a.36_p2.pdf is "System of the Finite Verb". Move it.
    path_36_p2 = os.path.join(ARTICLES_DIR, "07a.36 - The System of the Verb in Standard Biblical Prose", "07a.36_p2.pdf")
    if os.path.exists(path_36_p2):
        shutil.move(path_36_p2, os.path.join(MISFILED_DIR, "07a.XX_System_of_the_Finite_Verb.pdf"))

    # 07a.43: Move 07a.43.pdf (Semitic Studies cover) to misfiled
    path_43 = os.path.join(ARTICLES_DIR, "07a.43 - Conditional Particles in Biblical Hebrew Prose", "07a.43.pdf")
    if os.path.exists(path_43):
        shutil.move(path_43, os.path.join(MISFILED_DIR, "07a.43_Semitic_Studies_Cover.pdf"))

    print("Cleanup of misfiled PDFs complete.")

if __name__ == "__main__":
    main()
