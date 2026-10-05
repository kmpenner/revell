"""Item-level records, rights display, catalogue and workflow pages for the Revell site.

Runs after generate_site.py (and before build_search.py). It is idempotent.

1. metadata/records.json: one record per item, built from metadata/bibliography.json plus scan
   page counts and TEI presence. The rights fields (rights_status, rights_holder, rights_note,
   permission_requested, summary) are kept from the previous run, so edit them there by hand.
   rights_status is one of: pending, open, permission granted, restricted.
2. Rewrites each source transcription_tei.xml <teiHeader> with the bibliographic record and an
   <availability> statement, and copies it to docs/tei/<id>/.
3. Article pages get the real title, a record panel and a working TEI link. "restricted" items
   show the record and summary instead of the full text, as the Gatto proposal (s. 6) requires.
4. Writes docs/catalogue.html (every item, incl. books and book reviews) and docs/workflow.html,
   and adds both to the nav on every page.
"""
import glob, html, json, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
REC = os.path.join(ROOT, "metadata", "records.json")
RIGHTS_FIELDS = {"rights_status": "pending", "rights_holder": "", "rights_note": "", "permission_requested": "", "summary": ""}
STATUS_TEXT = {
    "pending": "Rights review in progress. Full text is shown provisionally for scholarly use.",
    "open": "Republished with no known restriction.",
    "permission granted": "Republished with the permission of the rights holder.",
    "restricted": "Full text not republished. Record and project summary only.",
}
esc = html.escape

bib = json.load(open(os.path.join(ROOT, "metadata", "bibliography.json")))
old = {r["id"]: r for r in json.load(open(REC))} if os.path.exists(REC) else {}


def item_id(key):  # "7.a.02" -> "07a.02"
    a, b, c = key.split(".")
    return f"{int(a):02d}{b}.{c}"


def parse(cit):
    m = re.match(r'\s*"(.+?)",?\s*(.*)$', cit)
    title, venue = (m.group(1).strip().rstrip(","), m.group(2).strip()) if m else (re.split(r"\.\s", cit, 1)[0], cit)
    y = re.findall(r"\b(19\d\d|20\d\d)\b", cit)
    pages = re.search(r"pp?\.\s*([\d\-–]+)", cit)
    return title, venue, (y[0] if y else ""), (pages.group(1) if pages else "")


def scan_pages(i):
    pdfs = [p for p in glob.glob(os.path.join(DOCS, "articles", f"{i}*.pdf"))]
    try:
        out = subprocess.run(["pdfinfo", pdfs[0]], capture_output=True, text=True).stdout if pdfs else ""
        return int(re.search(r"Pages:\s+(\d+)", out).group(1))
    except Exception:
        return None


def source_tei(i):
    hits = glob.glob(os.path.join(ROOT, "07a Articles", f"{i} - *", "transcription_tei.xml"))
    return hits[0] if hits else None


records = []
for key, cit in sorted(bib.items()):
    i = item_id(key)
    title, venue, year, pages = parse(cit)
    r = {"id": i, "type": "article" if ".a." in key else "book", "citation": cit, "title": title, "venue": venue,
         "year": year, "pages": pages, "scan_pages": scan_pages(i) if ".a." in key else None, "tei": bool(source_tei(i))}
    r.update({k: old.get(i, {}).get(k, v) for k, v in RIGHTS_FIELDS.items()})
    records.append(r)
for pdf in sorted(glob.glob(os.path.join(ROOT, "08 Book reviews", "*.pdf"))):
    i = "08." + re.sub(r"\W+", "_", os.path.splitext(os.path.basename(pdf))[0]).strip("_")
    r = {"id": i, "type": "review", "citation": "", "title": os.path.basename(pdf), "venue": "", "year": "", "pages": "",
         "scan_pages": None, "tei": False}
    r.update({k: old.get(i, {}).get(k, v) for k, v in RIGHTS_FIELDS.items()})
    records.append(r)
json.dump(records, open(REC, "w"), ensure_ascii=False, indent=1)
by_id = {r["id"]: r for r in records}

# --- 2. TEI headers ---------------------------------------------------------------------------
for r in records:
    src = source_tei(r["id"]) if r["type"] == "article" else None
    if not src:
        continue
    xml = open(src, encoding="utf-8").read()
    header = f"""<teiHeader>
    <fileDesc>
      <titleStmt>
        <title>{esc(r['title'])}</title>
        <author>Ernest John Revell</author>
        <respStmt><resp>Digitization and TEI encoding</resp><name>Revell Digital Corpus project, St. Francis Xavier University (Fr. Ed Gatto Chair of Christian Studies)</name></respStmt>
      </titleStmt>
      <publicationStmt>
        <publisher>Revell Digital Corpus</publisher>
        <idno type="corpus">{r['id']}</idno>
        <availability status="{'restricted' if r['rights_status'] in ('pending', 'restricted') else 'free'}">
          <p>Rights status: {esc(r['rights_status'])}. {esc(STATUS_TEXT[r['rights_status']])}{(' Rights holder: ' + esc(r['rights_holder']) + '.') if r['rights_holder'] else ''}</p>
        </availability>
      </publicationStmt>
      <sourceDesc>
        <bibl type="original">
          <author>E. J. Revell</author>
          <title level="a">{esc(r['title'])}</title>
          <title level="j">{esc(r['venue'])}</title>
          <date>{r['year']}</date>{f'''
          <biblScope unit="page">{esc(r['pages'])}</biblScope>''' if r['pages'] else ''}
        </bibl>
      </sourceDesc>
    </fileDesc>
  </teiHeader>"""
    new = re.sub(r"<teiHeader>.*?</teiHeader>", lambda _: header, xml, count=1, flags=re.S)
    if new != xml:
        open(src, "w", encoding="utf-8").write(new)
    dst = os.path.join(DOCS, "tei", r["id"])
    os.makedirs(dst, exist_ok=True)
    shutil.copyfile(src, os.path.join(dst, "transcription_tei.xml"))


# --- 3. Article pages -------------------------------------------------------------------------
def panel(r):
    rows = [("Citation", esc(r["citation"])), ("Venue", esc(r["venue"])), ("Year", r["year"]),
            ("Pages", esc(r["pages"]) or "&mdash;"), ("Scan", f"{r['scan_pages']} pages" if r["scan_pages"] else "&mdash;"),
            ("Rights", f"<strong>{esc(r['rights_status'])}</strong>: {esc(STATUS_TEXT[r['rights_status']])}"
                       + (f" Rights holder: {esc(r['rights_holder'])}." if r["rights_holder"] else ""))]
    body = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    return f'<div class="record-panel"><table class="record">{body}</table></div>'


for f in glob.glob(os.path.join(DOCS, "articles", "*.html")):
    i = os.path.basename(f).split("_")[0]
    r = by_id.get(i)
    if not r:
        continue
    page = open(f, encoding="utf-8").read()
    page = re.sub(r'<div class="record-panel">.*?</div>\s*', "", page, flags=re.S)  # idempotent
    page = re.sub(r"<h1>\d\da\.\d\d[^<]*</h1>", f"<h1>{esc(r['title'])}</h1>", page, count=1)
    page = page.replace("/transcription_tei.html\"", "/transcription_tei.xml\"").replace("📜 ", "")
    page = re.sub(r"(<p class=\"meta\">ID: [^<]*</p>.*?</header>)", lambda m: m.group(1) + "\n" + panel(r), page, count=1, flags=re.S)
    if r["rights_status"] == "restricted":
        summary = esc(r["summary"]) or "A project summary is in preparation."
        page = re.sub(r'<div class="content">.*?(</div>\s*</div>\s*</div>\s*</article>)',
                      lambda m: f'<div class="content"><h2>Summary</h2><p>{summary}</p><p>The full text is available through library holdings of <em>{esc(r["venue"])}</em>.</p></div>',
                      page, count=1, flags=re.S)
    page = re.sub(r"<title>[^<|]*\|", f"<title>{esc(r['title'])} |", page, count=1)
    open(f, "w", encoding="utf-8").write(page)

# --- 4. Catalogue, workflow, nav --------------------------------------------------------------
shell = open(os.path.join(DOCS, "biography.html"), encoding="utf-8").read()
head, rest = shell.split("<section>", 1)
foot = rest.split("</section>", 1)[1]


def page_html(title, body):
    return re.sub(r"<title>[^<|]*\|", f"<title>{title} |", head, count=1) \
        + "<section>\n" + body + "\n</section>" + foot


article_pages = {os.path.basename(p).split("_")[0]: os.path.basename(p) for p in glob.glob(os.path.join(DOCS, "articles", "*.html"))}
counts = {s: sum(1 for r in records if r["rights_status"] == s) for s in STATUS_TEXT}
total_pages = sum(r["scan_pages"] or 0 for r in records)


def table(kind):
    out = ['<table class="catalogue"><thead><tr><th>ID</th><th>Item</th><th>Year</th><th>Scan pp.</th><th>TEI</th><th>Rights</th></tr></thead><tbody>']
    for r in (x for x in records if x["type"] == kind):
        name = esc(r["title"])
        if r["id"] in article_pages:
            name = f'<a href="articles/{article_pages[r["id"]]}">{name}</a>'
        venue = f'<br><small>{esc(r["venue"])}</small>' if r["venue"] else ""
        tei = f'<a href="tei/{r["id"]}/transcription_tei.xml">XML</a>' if r["tei"] else "&mdash;"
        out.append(f'<tr><td>{r["id"]}</td><td>{name}{venue}</td><td>{r["year"]}</td><td>{r["scan_pages"] or ""}</td><td>{tei}</td><td>{esc(r["rights_status"])}</td></tr>')
    return "\n".join(out) + "</tbody></table>"


cat = f"""<h2>Catalogue</h2>
<p>Item-level records for every work in the corpus: {sum(1 for r in records if r['type']=='article')} articles
({total_pages} scanned pages), {sum(1 for r in records if r['type']=='book')} books and
{sum(1 for r in records if r['type']=='review')} book reviews. The records are also available as
<a href="records.json">records.json</a>.</p>
<p>Rights status: {', '.join(f'{v} {k}' for k, v in counts.items() if v)}. Each article is republished only after its
rights are reviewed. Restricted items show the record and a project summary instead of the full text.</p>
<h3>Articles (07a)</h3>
{table('article')}
<h3>Books (07b)</h3>
{table('book')}
<h3>Book reviews (08)</h3>
{table('review')}"""
open(os.path.join(DOCS, "catalogue.html"), "w", encoding="utf-8").write(page_html("Catalogue", cat))
shutil.copyfile(REC, os.path.join(DOCS, "records.json"))

wf = """<h2>Project workflow</h2>
<p>The Revell Digital Corpus is produced by student research assistants, following the pipeline set out in the
Fr. Ed Gatto Chair proposal (2026). This page documents it so that future students can continue and reuse the work.
The scripts live in the project repository's <code>scripts/</code> folder.</p>
<ol>
<li><strong>Inventory and metadata.</strong> Each item has an ID from Revell's own bibliography (07a = articles,
07b = books, 08 = book reviews), recorded in <code>metadata/bibliography.json</code>. <code>build_records.py</code>
turns it into <code>metadata/records.json</code>, the item-level record shown on the <a href="catalogue.html">catalogue</a>.</li>
<li><strong>Rights review.</strong> For each item, record the publisher or rights holder, its policy, and any
permission request in the item's <code>rights_*</code> fields of <code>records.json</code>. Status values:
<em>pending</em>, <em>open</em>, <em>permission granted</em>, <em>restricted</em>. A restricted item needs a
<code>summary</code>. The site then shows the record and summary instead of the text, and the scans stay internal.</li>
<li><strong>Archival scanning.</strong> Offprints are scanned at 400 dpi into <code>scans/</code>, then split and cropped
per article into <code>07a Articles/&lt;ID&gt; - &lt;short title&gt;/</code>.</li>
<li><strong>OCR and correction.</strong> AI-assisted OCR produces <code>transcription.md</code>. The student proofreads it
against the facsimile, with particular care for Hebrew vowel points and Masoretic accents.</li>
<li><strong>TEI encoding.</strong> <code>md_to_tei.py</code> wraps the corrected text in TEI P5: page breaks
(<code>&lt;pb/&gt;</code>), headings, notes, italics, and Hebrew marked as <code>&lt;foreign xml:lang="he"&gt;</code>.
<code>build_records.py</code> writes the bibliographic and rights record into the <code>teiHeader</code>.</li>
<li><strong>Validation.</strong> <code>validate_tei.py</code> checks every file against the TEI P5 schema
(<code>tei_all.rng</code>) and writes <code>reports/tei_validation.md</code>. Fix every error before publishing.</li>
<li><strong>Publication.</strong> Run <code>generate_site.py</code>, then <code>build_records.py</code>, then
<code>build_search.py</code>. Commit <code>docs/</code>, which GitHub Pages serves.</li>
</ol>"""
open(os.path.join(DOCS, "workflow.html"), "w", encoding="utf-8").write(page_html("Workflow", wf))

css = os.path.join(DOCS, "assets", "css", "style.css")
s = open(css, encoding="utf-8").read()
if ".record-panel" not in s:
    s += """
.record-panel { margin: 1rem 0; padding: .75rem 1rem; border: 1px solid #ccc; border-radius: 4px; background: #fafaf7; }
table.record th { text-align: left; padding-right: 1rem; vertical-align: top; white-space: nowrap; }
table.catalogue { width: 100%; border-collapse: collapse; font-size: .9rem; }
table.catalogue th, table.catalogue td { border-bottom: 1px solid #ddd; padding: .35rem .5rem; text-align: left; vertical-align: top; }
"""
    open(css, "w", encoding="utf-8").write(s)

for f in glob.glob(os.path.join(DOCS, "*.html")) + glob.glob(os.path.join(DOCS, "*", "*.html")):
    p = open(f, encoding="utf-8").read()
    if "catalogue.html\">Catalogue" in p:
        continue
    pre = "../" if os.path.dirname(f) != DOCS else ""
    p = re.sub(r'(<li><a href="[^"]*articles\.html">Articles</a></li>)',
               lambda m: f'<li><a href="{pre}catalogue.html">Catalogue</a></li>\n                    ' + m.group(1), p, count=1)
    p = re.sub(r'(<li><a href="[^"]*search\.html">Search</a></li>)',
               lambda m: m.group(1) + f'\n                    <li><a href="{pre}workflow.html">Workflow</a></li>', p, count=1)
    open(f, "w", encoding="utf-8").write(p)
print(f"{len(records)} records; rights: {counts}")
