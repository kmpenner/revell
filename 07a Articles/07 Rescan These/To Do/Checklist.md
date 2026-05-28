# Research Assistant Task List: Demarquis Moss

This document outlines the workflow and specific immediate tasks for the digitization of Professor E.J. Revell’s collected papers.

## Core Workflow Implementation

Follow this **"High Fidelity"** pipeline for each of the 53 articles located in `07a Articles/`.

### 1. Inventory & Metadata

- [ ] **Verify Master Catalog**: Ensure every folder in `07a Articles/` has a corresponding entry in `metadata/bibliography.json`.
- [ ] **Rights Review**: For each article, document the publisher and copyright status. Use the physical offprints as primary evidence for source details.

### 2. Archival Scanning

- [ ] **Audit Existing PDFs**: Check each folder (e.g., `07a.01`, `07a.02`) for a high-quality PDF scan.
- [ ] **Scan Missing/Low-Quality Items**:
  - [ ] Use the department scanner to produce **400 dpi** grayscale/color scans.
  - [ ] Save scans using the naming convention: `[ID]_[Shortened_Title].pdf` (e.g., `07a.01_Order_Elements_Verbal.pdf`).
  - [ ] Place all new scans in the respective article folders.

### 3. OCR & Linguistic QA (High Priority)

- [ ] **Run Initial OCR**: Use the `scripts/digitize_workflow.py` script to generate a base Markdown file if one does not exist.
  - *Command*: `python scripts/digitize_workflow.py`
- [ ] **Manual Proofreading**: This is the most critical step.
  - [ ] Open the generated `.md` file alongside the original PDF.
  - [ ] **Hebrew Verification**: Manually verify and correct all Hebrew text. Pay special attention to **Tiberian vocalization** and **Masoretic accents**.
  - [ ] Ensure that diacritics are accurately represented in Unicode.

### 4. TEI Encoding

- [ ] **Generate TEI-XML**: Use `scripts/batch_tei_transcription.py` to create the initial `transcription_tei.xml`.
- [ ] **Semantic Tagging**:
  - [ ] Encode structural levels (`<div>`, `<head>`, `<p>`).
  - [ ] Tag all biblical citations using `<cit><quote>...</quote><bibl>...</bibl></cit>`.
  - [ ] Use `<foreign xml:lang="he">` for all Hebrew text fragments.
  - [ ] Ensure footnotes are properly linked using `<note>` tags.

### 5. Validation & Site Preview

- [ ] **Build Preview**: Run the site generation script to see how the article renders.
  - *Command*: `python scripts/generate_site.py`
- [ ] **Visual Audit**: Verify that the Hebrew accents render correctly in the browser (check `docs/articles/[ID].html`).
- [ ] **Final Deposit**: Once validated, update the JSON metadata status to `complete`.

---

## Immediate Priorities (This Week)

1. **Audit 07a.01 -- 07a.10**: Ensure these first 10 articles have high-quality PDFs and initial OCR drafts.
2. **Correct Hebrew in 07a.49**: Finish the proofreading of "The Interpretative Significance of the Masoretic Punctuation" (currently in `draft` status).
3. **Update `bibliography.json`**: Add the publisher rights status for the first 20 articles.

---

## Specific Action Items (From Audit)

### Folder & File Integrity
- [ ] **Check for Incomplete Scans**: General audit of all 53 folders to ensure all pages are present.
- [ ] **Verify Folder Contents**: Ensure the correct PDF and Markdown files are in the correct article folders.
- [ ] **7a.15**: Verify if the article is only 1 page long or if pages are missing.
- [ ] **7a.32**: Confirm if the article starts on page 421.

### Rescans Required
- [ ] **7a.31**: 
  - [ ] **Missing pages**: 251, 255, 261.
  - [ ] **Requires rescanning**: 267, 269, 271.
- [ ] **7a.39**: Missing pages 76, 122, 168, and 300.
- [ ] **7a.44**: Fix/rescan the folded page.

### Wrong File Mappings
- [ ] **7a.20**: Currently contains files for `7a.30` and `7a.43`. Move to correct folders.
- [ ] **7a.23**: Currently contains files for `7a.34`. Fix mapping.
- [ ] **7a.28**: Verify if content is correct.
- [ ] **7a.30**: Currently contains files for `7a.37`. Fix mapping.

### Missing Articles
- [ ] **7a.11**: Not found.
- [ ] **7a.12**: Missing article file; folder incorrectly contains a "CURRICULUM VITAE" file.
- [ ] **7a.13**: Not found.
- [ ] **7a.26**: Not found.
- [ ] **7a.47**: Not found (noted as `7q.47` in logs).

