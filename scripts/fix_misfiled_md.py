
import os
import shutil
import re

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
    # 1. 07a.04.md (is 07a.28)
    move_file(r"07a.04 - New Biblical Fragment\07a.04.md", r"07a.28 - Pausal Phenomenon Biblical\07a.28.md")

    # 2. 07a.03_p2.md (is 07a.53)
    move_file(r"07a.03 - Sign Sound Study\07a.03_p2.md", r"07a.53 - Midian and Ishmael\07a.53.md")

    # 3. 07a.19_p8.md (is 07a.25, and it contains 19 articles)
    # Wait, 07a.19_p8.md was 07a.01_p2.md which turned out to be Stress (25).
    move_file(r"07a.19 - Pausal Forms Biblical Hebrew\07a.19_p8.md", r"07a.25 - Stress Waw Consecutive\07a.25_v2.md")

if __name__ == "__main__":
    main()
