"""Build docs/search.html and docs/search-index.json from the article transcription pages.

Client-side full-text search (no server), so it works on GitHub Pages. Hebrew is
indexed with and without points/accents, so a search for consonants alone matches
fully vocalized text. Run after the site generator: python3 scripts/build_search.py
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
bib = json.load(open(os.path.join(ROOT, "metadata", "bibliography.json")))

entries = []
for path in sorted(glob.glob(os.path.join(DOCS, "articles", "07a.*_transcription_tei.html"))):
    name = os.path.basename(path)
    m = re.match(r"07a\.(\d+)_transcription_tei\.html$", name)
    if not m:  # skip _p1/_p2 part files; the whole-article page carries the text
        continue
    num = m.group(1)
    page = open(path, encoding="utf-8").read()
    body = page.split('<div class="content">', 1)[-1]
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"\s+", " ", text).strip()
    ref = bib.get(f"7.a.{num}", "")
    title = re.match(r'"([^"]+)"', ref)
    entries.append({"id": f"07a.{num}", "url": f"articles/{name}",
                    "title": title.group(1) if title else f"Article 07a.{num}",
                    "ref": ref, "text": text})

json.dump(entries, open(os.path.join(DOCS, "search-index.json"), "w", encoding="utf-8"), ensure_ascii=False)

shell = open(os.path.join(DOCS, "articles.html"), encoding="utf-8").read()
head, _, rest = shell.partition("<section>")
_, _, tail = rest.partition("</section>")
nav_item = '<li><a href="search.html">Search</a></li>'
page = """<section>
<h2>Search the corpus</h2>
<p>Searches the full text of every transcribed article. Hebrew matches with or without vowel points and accents.</p>
<input id="q" type="search" placeholder="e.g. pausal, segol, &#1488;&#1514;&#1504;&#1495;" style="width:100%;font-size:1.1rem;padding:.5rem;box-sizing:border-box">
<p id="status" class="meta"></p>
<ol id="results"></ol>
<script>
const strip = s => s.normalize('NFD').replace(/[\\u0591-\\u05C7]/g, '').toLowerCase();
let idx = [];
fetch('search-index.json').then(r => r.json()).then(d => { idx = d.map(e => ({...e, plain: strip(e.text)})); document.getElementById('status').textContent = idx.length + ' articles indexed.'; run(); });
const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function run() {
  const q = strip(document.getElementById('q').value.trim()), out = document.getElementById('results');
  out.innerHTML = ''; if (q.length < 2) return;
  const hits = [];
  for (const e of idx) { let n = 0, i = -1, first = -1; while ((i = e.plain.indexOf(q, i + 1)) !== -1) { if (first < 0) first = i; n++; } if (n) hits.push([n, first, e]); }
  hits.sort((a, b) => b[0] - a[0]);
  document.getElementById('status').textContent = hits.length + ' of ' + idx.length + ' articles match.';
  for (const [n, first, e] of hits) {
    const s = Math.max(0, first - 80), snip = e.plain.slice(s, first + q.length + 80);
    const li = document.createElement('li');
    li.innerHTML = '<a href="' + e.url + '">' + esc(e.title) + '</a> <span class="meta">(' + e.id + ', ' + n + ' hit' + (n > 1 ? 's' : '') + ')</span><br><small>&hellip;' + esc(snip).split(esc(q)).join('<mark>' + esc(q) + '</mark>') + '&hellip;</small>';
    out.appendChild(li);
  }
}
document.getElementById('q').addEventListener('input', run);
const p = new URLSearchParams(location.search).get('q'); if (p) document.getElementById('q').value = p;
</script>
</section>"""
html_out = head.replace("<title>", "<title>Search | ", 1)
html_out = re.sub(r"<title>Search \| [^<]*</title>", "<title>Search | Revell Digital Corpus</title>", html_out)
if nav_item not in html_out:
    html_out = html_out.replace('<li><a href="biography.html">Biography</a></li>', '<li><a href="biography.html">Biography</a></li>\n                    ' + nav_item)
open(os.path.join(DOCS, "search.html"), "w", encoding="utf-8").write(html_out + page + tail)

# Add the Search link to every other page's nav (top-level and articles/ pages).
for f in glob.glob(os.path.join(DOCS, "*.html")) + glob.glob(os.path.join(DOCS, "*", "*.html")):
    s = open(f, encoding="utf-8").read()
    pre = "../" if os.path.dirname(f) != DOCS else ""
    item = f'<li><a href="{pre}search.html">Search</a></li>'
    bio = f'<li><a href="{pre}biography.html">Biography</a></li>'
    if item not in s and bio in s:
        open(f, "w", encoding="utf-8").write(s.replace(bio, bio + "\n                    " + item, 1))
print(len(entries), "articles indexed")
