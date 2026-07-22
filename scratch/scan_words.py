import re
import xml.etree.ElementTree as ET

file_path = '07a Articles/07a.02 - Clause Structure Prose/transcription_tei.xml'

# Let's read the file and parse it (ignoring the nested TEI tag for parsing purposes, or just reading as text)
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Temporarily strip nested TEI tags to make it parseable
content_clean = re.sub(r'<TEI\s+xmlns="http://www\.tei-c\.org/ns/1\.0">', '', content)
content_clean = re.sub(r'</TEI>', '', content_clean)

# Let's parse and get all text
try:
    root = ET.fromstring(content_clean)
except Exception as e:
    # If parsing fails, we split by tags and get text nodes manually
    print("Parsing failed, using token split:", e)

tokens = re.split(r'(<[^>]+>)', content)
text_content = []
for tok in tokens:
    if not tok.startswith('<'):
        text_content.append(tok)

full_text = " ".join(text_content)

# Find words with non-ascii characters or special punctuation used in Hebrew transliteration
# Transliterated Hebrew words often contain: ', ’, ʔ, š, ḥ, ʿ, ṣ, ṭ, Ț, κ, ʿ, etc. or are in all-caps
words = re.findall(r'\b[a-zA-Z\u0100-\u02AF\u1E00-\u1EFF\u0590-\u05FF0-9\-\[\]\']+\b', full_text)

candidates = set()
for w in words:
    # Check if the word contains any Hebrew transliteration character or is in uppercase and not standard English/Roman numerals
    # Standard English/Roman numerals: I, II, III, V, VIII, IX, X, etc.
    # Let's keep those containing special transliteration chars:
    if any(c in w for c in "’ʔšḥṣṭȚκʿ‘"):
        candidates.add(w)
    # Or uppercase words that are not short Roman numerals or common abbreviations
    elif w.isupper() and len(w) >= 2:
        if w not in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'BHK', 'E', 'J', 'REVELL', 'CLAUSE', 'STRUCTURE', 'QUMRAN', 'CAVE', 'MSS']:
            # Exclude purely grammatical notations (will handle separately)
            if not re.match(r'^(?:N|V|pN|pI|pt|Ns|Nˢ|Nª|hN|cV|cpt|cpN|cN|cNˢ|cNª|N\'|N’)+$', w):
                candidates.add(w)

print("Found candidate transliterated Hebrew words/phrases:")
for c in sorted(candidates):
    print(c)
