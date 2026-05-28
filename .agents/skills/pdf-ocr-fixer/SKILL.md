---
name: pdf-ocr-fixer
description: Corrects the text layer of a poorly OCR'd PDF using a clean Markdown file. Use this skill whenever a user asks to fix, replace, or align the text in a PDF with an .md file.
---

## Objective
Your task is to take a target `.pdf` and a corrected `.md` file, and generate a new `.pdf` where the visual layer is untouched, but the invisible searchable text layer is replaced by the clean text.

## Execution Rules
1. **Verify Dependencies:** Before doing anything, ensure `pymupdf` is installed in the current environment. If not, install it.
2. **Locate Script:** Use the Python script located at `scripts/align.py` within this skill directory.
3. **Run Command:** Execute the script using the arguments provided by the user: 
   `python .agents/skills/pdf-ocr-fixer/scripts/align.py <messy_pdf_path> <clean_md_path> <output_pdf_path>`
4. **Validation:** Confirm the output PDF was successfully generated. If the script throws an error regarding Markdown syntax, strip the Markdown formatting from the source file and try again.`
