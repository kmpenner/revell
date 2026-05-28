I. RESEARCH PROPOSAL

Project Title: The Revell Digital Corpus: A TEI Edition of Ernest John Revell’s Collected Papers

1. Project Summary

This project will preserve and make searchable the complete collection of scholarly articles by Professor
E.J. Revell (1934–2006) by digitizing his offprints, producing high-quality OCR text, encoding them in
TEI (Text Encoding Initiative) XML, and publishing them on a static website hosted on GitHub Pages.
E.J. Revell was a preeminent Canadian scholar of the Masoretic Text—the Hebrew text that forms the
basis of the Christian Old Testament. His articles on the "Palestinian Vocalization" and the Leningrad
Codex are foundational for biblical history and philology. The result will be a sustainable, citable digital
corpus usable for research and teaching in Christian studies, biblical linguistics, and digital humanities.

2. Problem Statement and Research Question

Problem: Professor Revell’s key insights are dispersed across more than 50 separate publications, many
of which are in out-of-print journals, Festschriften, or conference proceedings that are difficult to access.
While his work on the history of the Hebrew Bible is authoritative, it is effectively invisible to modern
digital tools. Standard PDF scanning is insufficient for this material because Revell’s work relies heavily
on Tiberian Hebrew vocalization and complex Masoretic accents; standard Optical Character
Recognition (OCR) reduces this linguistic data to unsearchable gibberish.
Research Question: What new scholarly connections become possible when Revell’s dispersed papers
are unified into a single, structurally encoded, and searchable dataset?
Claim: Creating a TEI-encoded corpus will materially improve access, citation accuracy, and the ability
of theologians and historians to trace specific grammatical and Masoretic themes across Revell’s
lifetime of work. This directly supports the Gatto Chair’s objective of the "scholarly exploration of
Christianity from all perspectives," specifically the historical and literary analysis of the Church’s
scriptures.

3. Literature Review and Significance

Digital preservation is common, but scholarly digitization of complex non-Latin scripts remains rare.

?  Why PDF is insufficient: A simple scan of an article like "The Oldest Evidence of the Hebrew
Accent System" (1971) does not allow a user to search for specific Hebrew accent patterns.

?  Why TEI matters: The Text Encoding Initiative (TEI) is the international standard for

representing scholarly texts. It allows us to tag the function of text—distinguishing between a
"biblical citation," a "grammatical rule," and a "footnote."

?  Durability: By publishing as a static site on GitHub, we ensure the project is immune to "link rot"
and platform obsolescence, serving the Christian Studies community indefinitely without ongoing
maintenance costs.

4. Research Design and Methodology

The workflow will be executed by a student Research Assistant (RA) trained in my Digital Methods for
Historical Documents course. The process follows a strict "High Fidelity" pipeline:

1.  Inventory & Metadata: Create a master catalog of the ~53 articles, establishing bibliographic

metadata and specific rights status for each venue.

2.  Archival Scanning: Produce high-resolution scans (400 dpi) of the physical offprints.
3.  OCR & Correction: Run AI-assisted OCR to generate raw text. Crucially, the student will

manually proofread the Hebrew text to ensure Masoretic accents are faithfully reproduced—a task
requiring specialised training in Hebrew cantillation symbols provided in the Religious Studies
program.

4.  TEI Encoding: The corrected text will be wrapped in TEI-XML tags using a custom ODD (One

Document Does it all) profile to encode structural divisions, biblical citations, and foreign language
shifts.

5.  Publication: A build script will transform the TEI XML into HTML for the public GitHub Pages

site.

5. Outputs

The project will deliver: (i) validated TEI XML files for each article eligible for republication; (ii) item-
level metadata records for about 850 pages of scholarship; (iii) a public GitHub Pages site with browse
and search functionality; and (iv) a documented workflow to support future student training and reuse.

6. Copyright and Ethical Considerations

Because this project includes 20th-century publications that may remain under copyright, rights review
is built into the workflow. I have physical custody of the offprints through the Revell estate, which
enables preservation scanning and scholarly processing; however, public republication will proceed
item-by-item based on documented rights status and permissions. For each article, the Research
Assistant will record the source, publisher, and rights statements, and we will seek permission where
required. Items that can be lawfully republished will appear on the public website as full text. Where
republishing rights cannot be secured, the site will provide a complete metadata record and a project-
generated summary, with links to library access. Preservation scans for restricted items will be retained
for internal project use only, consistent with institutional policy and applicable fair dealing provisions.

7. Timeline (May – July 2026)

?  Week 1: Inventory, rights assessment start, and pilot encoding.
?  Weeks 2–7: Bulk scanning, OCR correction, and linguistic QA of the 53 articles (~850 pages).
?  Weeks 8–9: TEI encoding and metadata completion.
?  Week 10: Site build, validation, and final deposit.

8. Relation to Teaching and Future Work

This project serves as a practical lab for the Digital Methods curriculum at StFX. It establishes the
infrastructure for future digitization of Canadian theological scholarship, directly benefiting the
Department of Religious Studies and the broader Humanities faculty.

II. REFERENCES / BIBLIOGRAPHY

Primary Sources (Sample of Articles to be Digitized)

1.  Revell, E.J. "The Order of the Elements in the Verbal Statement Clause in 1Q Serek." Revue de

Qumran 3 (1962): 559-569.

2.  Revell, E.J. "A New Biblical Fragment with Palestinian Vocalization." Textus VII (1969): 59-75.
3.  Revell, E.J. "The Oldest Evidence of the Hebrew Accent System." Bulletin of the John Rylands

Library 54 (1971): 214-222.

4.  Revell, E.J. "Pausal Forms in Biblical Hebrew: their function, origin, and significance." Journal of

Semitic Studies XXV (1980): 165-179.

5.  Revell, E.J. "The Leningrad Codex as a Representative of the Masoretic Text." Introduction to the

Facsimile Edition, Eerdmans, 1997.

Methodological Standards

1.  TEI Consortium. TEI P5: Guidelines for Electronic Text Encoding and Interchange. Version 4.7.0.

2023.

2.  Holmes, Martin. "The Guidelines of the Text Encoding Initiative." Scholarly Editing: The Annual

of the Association for Documentary Editing 38 (2017).

3.  Burnard, Lou. What is the Text Encoding Initiative? OpenEdition Press, 2014.

III. RESEARCH CONTRIBUTIONS

A. Contributions (published or accepted) in the last 7 years (2019–2026)

A1. Published or accepted refereed publications (books, monographs, book chapters, articles)

?  Penner, K. (2026). Lexham English Dead Sea Scrolls. Accepted. Lexham Press (Bellingham, WA).
?  Penner, K.; Scott, I.; Zacharias, D.; Brannan, R. (2026). Lexham English Pseudepigrapha.

Accepted. Lexham Press (Bellingham, WA).

?  Penner, K. (2026). “Evaluating AI for the Digital Scholarly Edition: Tools for Translation and
Interpretive Commentary.” In D. Estes (ed.), Artificial Intelligence for Bible Translation and
Interpretation, 153–189. In press. T&T Clark (London).

?  Penner, K.; Brannan, R.; Scott, I.; Zacharias, H.; Heiser, M. (eds.). (2024). Lexham Old Testament

Pseudepigrapha. Accepted. Lexham Press (Bellingham, WA).

?  Penner, K.; Pass, B. (2022). “The Value of Codex Marchalianus for the Greek Text of Isaiah.”

Journal of Septuagint and Cognate Studies 55: 103–133.

?  Penner, K. (2021). “The Significance of the Biblical Hebrew Verb Forms.” In J. Naudé and C.

Miller (eds.), Linguistic Approaches to Tense, Aspect, and Modality in the Biblical Hebrew Verbal
System. Accepted. Eisenbrauns (Winona Lake, IN).

?  Penner, K. (2021). “The Significance of the Finite Verb Conjugations in the Hebrew Dead Sea

Scrolls.” In S. Fassberg (ed.), Hebrew Texts and Language of the Second Temple Period, 204–235.
Brill (Leiden).

?  Penner, K. (2021). “Faith in Greek Isaiah.” In S. Rochester and J. Lee (eds.), Scriptures,

Scholarship, and the People of God, 136–148. Regent College (Vancouver).
?  Penner, K. (2020). Isaiah. Brill Septuagint Commentary Series. Brill (Leiden).
?  Penner, K. (2020). “The Tree of Life in Enochic Literature.” In D. Estes (ed.), The Tree of Life,

166–182. Brill (Leiden).

?  Penner, K. (2019). “Philo’s Eschatology, Personal and Cosmic.” Journal for the Study of Judaism

50: 383–402.

?  Penner, K. (2019). “Ancient Names for Hebrew and Aramaic: A Case for Lexical Revision.” New

Testament Studies 65: 412–423.

?  Penner, K. (2019). “?????, ???????, ?????????.” In Historical and Theological Lexicon of the

Septuagint, vol. 1, 1364–1377. Mohr Siebeck (Tübingen).

A2. Other refereed contributions (e.g., papers presented at scholarly meetings or conferences)

?  Penner, K. (2025). “Orthographic Variations and Phonological Evolution: A Study Based on Codex
Sinaiticus and Codex Marchalianus.” Septuagint Within the History of Greek, Sydney, Australia.
(Competitive: Yes.)

?  Penner, K. (2019). “Evidence for Hebrew Phonology from the Biblical Dead Sea Scrolls.” Society

of Biblical Literature Annual Meeting, San Diego, USA.

A3. Other contributions (research reports, public lectures, creative works, etc.)

?  Penner, K. (2022). “A Toolkit for Humanities Research and Editing Ancient Documents.” Digital

Humanities Summer Institute East, Antigonish, Canada. (Invited keynote.)

?  Penner, K. (2023). Review of Aspect, Communicative Appeal, and Temporal Meaning in Biblical

Hebrew Verbal Forms. Review of Biblical Literature (2023-06-09).

?  Penner, K. (2021–2022). Secretary, Board of Directors, Text Encoding Initiative (TEI).
?  Penner, K. (2019– ). Series Co-Editor, Digital Biblical Studies.
?  Penner, K. (2019– ). General Editor, Lexham English Septuagint.

B. Up to five most significant research contributions not included in A above

?  Penner, K. (2015). The Verbal System of the Dead Sea Scrolls: Tense, Aspect, and Modality in

Qumran Hebrew Texts. Brill (Leiden).

?  Penner, K. (2014). “Did the Midrash of Shemihazai and Azael use the Book of Giants?” In J.

Charlesworth and L. McDonald (eds.), Sacra Scriptura: How “Non-Canonical” Texts Functioned
in Early Judaism and Early Christianity, 15–45. T&T Clark.

?  Penner, K. (2010). “Citation Formulae as Indices to Canonicity in Early Jewish and Early Christian
Literature.” In J. Charlesworth and L. McDonald (eds.), Jewish and Christian Scriptures: The
Function of “Canonical” and “Non-Canonical” Religious Texts, 62–84. T&T Clark.

?  Penner, K. (2012). “Sinaiticus Corrector Cb2 as a Witness to the Alexandrian Text of Isaiah.”

Journal of Septuagint and Cognate Studies 45: 23–38.

?  Penner, K. (2012). Contributing co-editor and translator for multiple books in Lexham English

Septuagint (Lexham Press).

IV. BUDGET JUSTIFICATION

1. Employment of Assistants

Position: 1 Undergraduate Student Research Assistant (Summer)

Rate: $18.00/hr + 11% vacation/benefits = $19.98/hr

Hours: 350 hours (10 weeks × 35 hrs/week)

Total Request: $6,993.00

?  Functions & Tasks:

The student will execute the digitization pipeline for the Revell Article Corpus.
?  Inventory & Rights Management (50 hours): Cataloging the 53 articles and managing the

permissions process for multiple journals and publishers.

?  Scanning (20 hours): Producing high-resolution archival scans of the offprints.
?  OCR Correction & Linguistic QA (200 hours): This is the primary labour cost. The student

must manually verify the AI-generated Hebrew text. The complexity of Revell’s work
(Tiberian vowels and accents) requires a human editor to distinguish between similar Hebrew
glyphs to ensure the digital edition is philologically accurate.

?  TEI Encoding & Metadata (60 hours): Wrapping the corrected text in semantic XML tags

(citations, footnotes) and creating bibliographic metadata.

?  Site Build & Documentation (20 hours): Configuring the GitHub repository and writing the

project documentation.

?  Educational & Research Training Benefit:

This position offers high-level training in Digital Humanities and Biblical Philology. The student
(who has completed Digital Methods for Historical Documents) will move beyond theory to
professional practice. They will gain marketable skills in:
?  Text Encoding Initiative (TEI): The global standard for digital scholarly editions.
?  Intellectual Property Management: Navigating copyright for legacy scholarly works.
?  Data Management: Handling complex linguistic datasets.

2. Equipment & Supplies

Request: $0.00
We will utilize existing scanning hardware in the Department of Religious Studies and open-source
software (GitHub Pages, VS Code) to minimize costs.

3. Total Budget Request

$6,993.00


