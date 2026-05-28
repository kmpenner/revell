# Project Review: The Revell Digital Corpus

**Date:** May 5, 2026
**Meeting:** Ken Penner (PI) & Demarquis Moss (RA)

## 1. Project Purpose
The primary goal is to create a **high-fidelity digital edition** of the collected scholarly papers of **Ernest John Revell** (1934–2006).

### Why This Matters
*   **Access:** Revell's insights are dispersed across 50+ out-of-print journals and *Festschriften*.
*   **Technical Challenge:** Standard OCR fails on Masoretic Hebrew (vowels and accents). This project uses human-corrected OCR and **TEI (Text Encoding Initiative) XML** to preserve the linguistic data accurately.
*   **Searchability:** By encoding the text structurally, we enable searches for specific grammatical rules, biblical citations, and accent patterns.
*   **Legacy:** A sustainable, citable corpus hosted on GitHub Pages for the Christian studies and biblical linguistics community.

## 2. Project Timeline (Summer 2026)
The project is scheduled for **10 weeks**, running from early May to mid-July.

| Phase       | Timeline             | Primary Tasks                                                   |
| :---------- | :------------------- | :-------------------------------------------------------------- |
| **Phase 1** | **Week 1** (Current) | Inventory, Rights Assessment, Pilot Encoding.                   |
| **Phase 2** | **Weeks 2–7**        | Bulk Scanning, OCR Correction, Linguistic QA (Hebrew proofing). |
| **Phase 3** | **Weeks 8–9**        | TEI Encoding & Metadata Completion.                             |
| **Phase 4** | **Week 10**          | Site Build, Validation, Final Deposit to GitHub.                |

## 3. Current Status (Week 1)
*   **Cataloging:** The `metadata/bibliography.json` is complete, listing **53 articles** (7.a) and **7 books/editions** (7.b).
*   **Infrastructure:** Directory structure is established with folders for all 53 articles.
*   **Preliminary Work:** Raw OCR was generated for many files in Feb 2026.
*   **Gaps Identified:**
    *   **Missing PDFs:** Folders 7.a.11, 13, 26, 38, and 40 currently have no PDF files.
    *   **Duplicate PDFs:** Folders 7.a.12, 36, 42, and 47 have multiple PDF fragments needing merging or selection.

## 4. PI Decisions & Immediate Tasks
*   **Rights Assessment:** Ignored for this phase (Revell holds copyright for all items).
*   **Missing Scans:** PI (Ken Penner) will take the lead on locating these.
*   **TEI Encoding:** Delayed for RA until PI establishes a recommended LLM workflow.

## 5. Day 1 Assignment for Demarquis Moss
The first day focuses on **Inventory Cleanup and Structural Audit** to prepare the corpus for linguistic QA.

### Task A: Folder & PDF Reconciliation
Reconcile folders containing multiple or fragmented PDFs to ensure a single "Source of Truth" for each article.
*   **Target Folders:** `07a.12`, `07a.36`, `07a.42`, and `07a.47` (6 PDFs).
*   **Deliverable:** One definitive PDF (or a clearly named sequence) per folder and a brief `inventory.txt` note explaining the selection.

### Task B: Logical OCR Cleanup (Article 07a.03)
Fix a major "splicing" error in the OCR for *"Sign and Sound in the Study of Written Texts"*.
*   **Issue:** A section on Old English adjectives (lines 53–86) has been misfiled into this article.
*   **Deliverable:** A cleaned `.md` file that matches the logic and flow of the source PDF.

### Task C: Technical Setup & Hebrew Gap Analysis
*   **Setup:**
    *   Ensure VS Code is configured with **SBL Hebrew** fonts and a Hebrew-friendly keyboard layout.
    *   Download and install **Folio PDF Reader and Editor** (by Adel Hashemi) for PDF editing tasks.
*   **Audit:** Perform a "Gap Analysis" on `07a.01`. Identify every instance of OCR gibberish (e.g., `!2?`) and create a `gap_log.md` with screenshots of the corresponding Hebrew characters from the PDF.
