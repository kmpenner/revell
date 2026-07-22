# Implementation Plan - Format transcription_tei.xml for Sign Sound Study

This plan details the steps to correct and format the TEI XML transcription file [transcription_tei.xml](file:///Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a%20Articles/07a.03%20-%20Sign%20Sound%20Study/transcription_tei.xml) for E. J. Revell's article *"Sign and Sound in the Study of Written Texts"*.

## Context & Key Findings
1. **Misplaced Pages**: The current `transcription_tei.xml` is based on an odd-pages-only reject scan (`07a.03-reject.pdf`). It contains:
   - Page 23 of an article by Peters (*"Old English Adverb Subsets"*)
   - Page 1 of an article by P.M. Austin (*"The Etymology of 'King' in Soviet Turkic Languages"*)
2. **Missing Pages**: The actual article by E. J. Revell runs from journal page 24 to 33, but pages 28 and 29 are completely missing, and pages 32 and 33 are truncated/mangled.
3. **Correct Source**: The file [07a.03.pdf](file:///Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a%20Articles/07a.03%20-%20Sign%20Sound%20Study/07a.03.pdf) contains the full pages. We have extracted its full text in the scratch directory to reconstruct the complete article.

---

## User Review Required

> [!IMPORTANT]
> - **Remove Non-Revell Pages**: We will exclude Peters (Page 23) and Austin (Page 1) from the final XML because they are from different articles that were scanned together in the journal volume.
> - **Page Range Correction**: We will correct the publication page range in `<biblScope>` from `24-30` to `24-33` to match the actual article span.

---

## Open Questions
There are no major open questions. The document structure is clear, and we have the full text from the PDF.

---

## Proposed Changes

### Articles Component

#### [MODIFY] [transcription_tei.xml](file:///Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a%20Articles/07a.03%20-%20Sign%20Sound%20Study/transcription_tei.xml)
- Update `<teiHeader>` metadata (correct page range to `24-33`).
- Clean the text body to only include E. J. Revell's article (pages 24 to 33).
- Reconstruct the missing sections (Section 8, Section 9.1, and the full endings of Section 10 and 11).
- Place all footnotes (1 to 34) inline as `<note place="foot" n="XX"><p>...</p></note>`.
- Standardize running headers and footers into `<fw type="header" place="top">` or `<fw type="footer">` tags.
- Standardize formatting tags (e.g. convert `<emph>` to `<hi rend="italic">` or wrap linguistic terms in `<term>` where appropriate).

---

## Verification Plan

### Automated Tests
- Run a Python verification script to parse the output XML using `xml.etree.ElementTree` to ensure it is well-formed.
- Run `python scripts/generate_site.py` to compile the site and check if the article builds successfully without errors.

### Manual Verification
- Verify the compiled HTML output in `docs/articles/07a.03_transcription_tei.html` to confirm that page numbers, formatting, and footnotes are displayed correctly.
