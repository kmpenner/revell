import re
import os
import xml.etree.ElementTree as ET

file_path = '07a Articles/07a.02 - Clause Structure Prose/transcription_tei.xml'
output_path = '07a Articles/07a.02 - Clause Structure Prose/transcription_tei.xml'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# Make backup first
with open(file_path + '.bak', 'w', encoding='utf-8') as f:
    f.write(content)

print("Original length:", len(content))

# --- STEP 1: Fix Footnote 30 and 31 Syntax Errors ---
# We use a robust regex to find and replace the malformed footnote block
pattern_fn = r'<note\s+place="foot"\s+n="30">.*?</note>\s*<note\s+place="foot"\s+n="31">.*?</note></hi>\s*I,\s*13,\s*one\s*in\s*<hi>\s*1\s*Q\s*S\s*</hi>\s*III,\s*26\.\s*</p>\s*</note>\s*<note\s+place="foot"\s+n="31">.*?</note>'

new_footnote_block = """            <note
                place="foot" n="30">
                <p>Two examples in <hi rend="italic">1 Q M</hi> I, 13, one in <hi rend="italic">1 Q S</hi> III, 26.</p>
            </note>
            <note
                place="foot" n="31">
                <p><hi rend="italic">1 Q M</hi> II, 3, and <hi rend="italic">1 Q p Hab</hi> IV, 12 (reading <term xml:lang="hbo-Latn">mwhlḥ[hmh z]h</term> ).</p>
            </note>"""

content, count = re.subn(pattern_fn, new_footnote_block, content, flags=re.DOTALL)
print(f"Step 1: Footnotes corrected using regex. Count: {count}")

# --- STEP 2: Remove Nested TEI Tags ---
# We target the nested tags by matching their specific indentation or surrounding elements to avoid matching root tags
pattern_tei_open = r'\n\s+<TEI\s+xmlns="http://www\.tei-c\.org/ns/1\.0"\s*>'
content, count_open = re.subn(pattern_tei_open, '', content)
print(f"Step 2a: Nested <TEI> opening tag removed. Count: {count_open}")

pattern_tei_close = r'</list>\s*</TEI>\s*<pb\s+n="19"\s*/>'
content, count_close = re.subn(pattern_tei_close, '</list>\n            <pb n="19" />', content)
print(f"Step 2b: Nested </TEI> closing tag removed. Count: {count_close}")


# --- STEP 3 & 4 & 5: Wrap Scrolls, Hebrew Terms, and Grammatical Terms ---
scrolls = [
    '1 Q Serek', '1 Q Milḥamah', '1 Q S', '1 Q M', '1 Q Sa', '1 Q Sb', '1 Q p Hab',
    '1 Q 14', '1 Q 16', '1 Q 17', '1 Q 18', '1 Q 19', '1 Q 22', '1 Q 26', '1 Q 29'
]

hebrew_phrases = [
    "wz'wm hw'h bmšrt 'šmtw",
    "WKmŠpT hZhl kWl hNWSp lYhD",
    "lmŠkyl lhBYn wllMD",
    "lhBYn wllMD",
    "lmŠkyl lBRK",
    "wbḥ [šws] rwt",
    "mry'ym",
    "’RWR HB' BGLWLY LBW L'BWR",
    "'RWR HB' BGLWLY LBW L'BWR",
    "BGLWLY LBW L'BWR",
    "BRYT, YTBRK, YHY",
    "'LH, WHTBRK, YHYH",
    "zH HSrk",
    "'WRKYH KWL H'DH",
    "'NW 'M QWDSKH",
    "HYWM MW'DW",
    "W['TH] 'L 'BWTYNW",
    "W'NW 'M [GWR]L[KH]",
    "wh'yš... yšlhhw",
    "yršh bndbh",
    "y- /-šlhhw",
    "pšrw / hqryh / hy' / yrwšlm",
    "wl'wš byd rmh lw' yšwb 'wd",
    "mwhlḥ[hmh z]h",
    "(w)n' nš",
    "wlw’ lnw, bkwḥkh, wb‘wz ḥylkh hgdwl",
    "w’šR ydbR bpyhw dbR nbl šlwšh ḥwdšYM",
    "HY'H 'T ... LMDBR",
    "WKN LNWQM LNPŠW KWL DBR",
    "LW' LHWKYḤ",
    "B'T HZW'T",
    "MKWL 'WL",
    "wlkwl gbwryhm 'yn m'md",
    "w'yn 'wzr lw",
    "w'yn sn'h",
    "wmN’[wryw ll]mdhw",
    "wlw’ lswr",
    "w’yn ls’wd",
    "wyhκyn pʿmyw",
    "wkly MLḤMWTM / HMH / MWR'M",
    "H'YŠ HNS'L / Y- / -DBR BTRW",
    "hdgl hmtqrb / kwlm / šB' m'rkwt",
    "kwl hb' ... / kwl 'yš mh mh... / y- /-šlhhw",
    "lmŠkyl", "lhBYn", "wllMD", "lBRK", "sbyb", "z'wm", "hw'h", "bmšrt", "'šmtw",
    "BRWK", "'RWR", "z'WM", "BRYK", "’RWR", "z’WM", "BRYT", "YTBRK", "YHY",
    "’LH", "WHTBRK", "YHYH", "zH", "HSrk", "srk", "'WRKYH", "KWL", "H'DH",
    "’NW", "’M", "QWDSKH", "HYWM", "MW'DW", "W['TH]", "’L", "’BWTYNW", "W'NW",
    "[GWR]L[KH]", "wh'yš", "yšlhhw", "yršh", "bndbh", "pšrw", "hqryh", "hy'", "yrwšlm",
    "wl'wš", "byd", "rmh", "lw'", "yšwb", "'wd", "ylḥmw", "n' nš", "nš", "wmwbdl",
    "wlw’", "lnw", "bkwḥkh", "wb‘wz", "ḥylkh", "hgdwl", "w’šR", "ydbR", "bpyhw", "dbR",
    "nbl", "šlwšh", "ḥwdšYM", "HY'H", "'T", "LMDBR", "WKN", "LNWQM", "LNPŠW", "DBR",
    "LW'", "LHWKYḤ", "B'T", "HZW'T", "MKWL", "'WL", "wlkwl", "gbwryhm", "'yn", "m'md",
    "w'yn", "'wzr", "lw", "sn'h", "wmN’[wryw", "ll]mdhw", "wl[qḥt]", "lswr", "ls’wd",
    "wyhκyn", "pʿmyw", "wkly", "MLḤMWTM", "HMH", "MWR'M", "H'YŠ", "HNS'L", "BTRW",
    "hdgl", "hmtqrb", "kwlm", "šB'", "m'rkwt", "kwl", "hb'", "’yš", "mh", "yšlhhw",
    "hwnm", "’xn", "’šn", "'ŠR", "’šR", "’ŠR", "’šR", "KY'", "ʔš", "’YH", "’WD", "'YH", "'WD",
    "'YN", "YŠ", "NḤLT", "BLTY", "BKN", "mwhlḥ[hmh", "nš", "bbšrw", "wbšnyt", "wbḥ", "wl[qḥt",
    "mṣtyhmh", "šdqw", "šlhhw", "šws", "ḤWR", "ḥbḥn", "ḥwmt", "ḥwqym"
]

single_grammatical = [
    "pN", "pI", "pt", "Ns", "Nˢ", "Nª", "hN", "cV", "cpt", "cpN", "cN", "cNˢ", "cNª", "N'", "N’", "N", "V"
]

# Find combinations in file
tokens_scan = re.split(r'(<[^>]+>)', content)
detected_combinations = set()
for tok in tokens_scan:
    if not tok.startswith('<'):
        matches = re.findall(r'\b[A-Za-zˢª\']+(?:-[A-Za-zˢª\']+)+\b', tok)
        for m in matches:
            parts = m.split('-')
            if all(p in single_grammatical for p in parts):
                detected_combinations.add(m)

print("Detected combinations:", sorted(detected_combinations))
grammatical_terms = list(detected_combinations) + single_grammatical

# Compile lists and sets for matching
scrolls_set = set(scrolls)
hebrew_set = set(hebrew_phrases)
gram_set = set(grammatical_terms)

# Word character class definition
word_chars_class = r'[a-zA-Z\u0100-\u02AF\u1E00-\u1EFF\u0590-\u05FF0-9\-\[\]\'\’\ʔ\š\ḥ\ʿ\ṣ\ṭ\Ț\κ\ˢ\ª]'

# 1. First Pass: Replace Multi-Word Phrases outside tags
phrases_with_spaces = [p for p in hebrew_set | scrolls_set if any(c in p for c in " /.,()")]
phrases_with_spaces = sorted(phrases_with_spaces, key=len, reverse=True)

print(f"Replacing {len(phrases_with_spaces)} multi-word phrases...")

def replace_phrase_outside_tags(text, phrase, template):
    parts = re.split(r'(<[^>]+>)', text)
    term_depth = 0
    hi_depth = 0
    for idx in range(len(parts)):
        part = parts[idx]
        if part.startswith('<'):
            if part.startswith('<term'):
                term_depth += 1
            elif part == '</term>':
                term_depth -= 1
            elif part.startswith('<hi'):
                hi_depth += 1
            elif part == '</hi>':
                hi_depth -= 1
        else:
            is_scroll = ("italic" in template)
            should_replace = (hi_depth == 0 and term_depth == 0) if is_scroll else (term_depth == 0)
            if should_replace:
                # Optimized check: only compile regex and sub if the phrase is present in this text part
                if phrase in part:
                    pattern = rf'(?<!{word_chars_class})' + re.escape(phrase) + rf'(?!{word_chars_class})'
                    parts[idx] = re.sub(pattern, lambda m: template.format(m.group(0)), part)
    return "".join(parts)

# Run phrase replacements
for phrase in phrases_with_spaces:
    template = '<hi rend="italic">{}</hi>' if phrase in scrolls_set else '<term xml:lang="hbo-Latn">{}</term>'
    content = replace_phrase_outside_tags(content, phrase, template)

# 2. Second Pass: Replace Single Words using a single fast regex scan on text runs
single_words = [w for w in (scrolls_set | hebrew_set | gram_set) if not any(c in w for c in " /.,()")]
single_words_set = set(single_words)

# Build a fast compiled regex to match any word run in text
word_regex = re.compile(rf'[a-zA-Z\u0100-\u02AF\u1E00-\u1EFF\u0590-\u05FF0-9\-\[\]\'\’\ʔ\š\ḥ\ʿ\ṣ\ṭ\Ț\κ\ˢ\ª]+')

parts = re.split(r'(<[^>]+>)', content)
term_depth = 0
hi_depth = 0

print("Scanning and replacing single words...")

for idx in range(len(parts)):
    part = parts[idx]
    if part.startswith('<'):
        if part.startswith('<term'):
            term_depth += 1
        elif part == '</term>':
            term_depth -= 1
        elif part.startswith('<hi'):
            hi_depth += 1
        elif part == '</hi>':
            hi_depth -= 1
    else:
        # Replace individual words
        if len(part.strip()) > 0:
            def word_repl(match):
                w = match.group(0)
                if w in scrolls_set:
                    if hi_depth == 0 and term_depth == 0:
                        return f'<hi rend="italic">{w}</hi>'
                elif w in hebrew_set or w in gram_set:
                    if term_depth == 0:
                        return f'<term xml:lang="hbo-Latn">{w}</term>'
                return w
            parts[idx] = word_regex.sub(word_repl, part)

content = "".join(parts)

# --- STEP 6: Normalize superscript notations ---
content = content.replace('Ns', 'N<hi rend="sup">s</hi>')
content = content.replace('Nˢ', 'N<hi rend="sup">s</hi>')
content = content.replace('Nª', 'N<hi rend="sup">a</hi>')
content = content.replace('cNs', 'cN<hi rend="sup">s</hi>')
content = content.replace('cNˢ', 'cN<hi rend="sup">s</hi>')
content = content.replace('cNª', 'cN<hi rend="sup">a</hi>')
content = re.sub(r'<hi\s+rend="superscript"\s*>\s*([a-zA-Z0-9]+)\s*</hi>', r'<hi rend="sup">\1</hi>', content, flags=re.IGNORECASE | re.DOTALL)
content = re.sub(r'<sup\s*>\s*([a-zA-Z0-9]+)\s*</sup>', r'<hi rend="sup">\1</hi>', content, flags=re.IGNORECASE | re.DOTALL)
# --- STEP 7: Replace running headers with <fw> elements ---
content = re.sub(r'<head>\s*E\.\s*J\.\s*REVELL\s*</head>', r'<fw type="header" place="top">E. J. REVELL</fw>', content, flags=re.IGNORECASE | re.DOTALL)
content = re.sub(r'<head>\s*CLAUSE\s+STRUCTURE\s+IN\s+QUMRAN\s+CAVE\s+I\s*</head>', r'<fw type="header" place="top">CLAUSE STRUCTURE IN QUMRAN CAVE I</fw>', content, flags=re.IGNORECASE | re.DOTALL)



# Flatten any nested term elements
output = []
depth = 0
rebuilt_tokens = re.split(r'(</?term(?: [^>]*)?>)', content)
for tok in rebuilt_tokens:
    if tok.startswith('<term'):
        if depth == 0:
            output.append(tok)
        depth += 1
    elif tok == '</term>':
        depth -= 1
        if depth == 0:
            output.append(tok)
    else:
        output.append(tok)

final_content = "".join(output)

# Verify well-formedness
try:
    ET.fromstring(final_content)
    print("Verification: XML parsed successfully! Well-formedness check passed.")
except Exception as e:
    print("Verification: XML parsing failed:", e)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Formatting script completed successfully.")
