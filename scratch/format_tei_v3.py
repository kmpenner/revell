import re

file_path = '07a Articles/07a.02 - Clause Structure Prose/transcription_tei.xml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make backup first
with open(file_path + '.bak', 'w', encoding='utf-8') as f:
    f.write(content)

# 1. Strip nested TEI tags first (before splitting)
content = re.sub(r'<TEI\s+xmlns="http://www\.tei-c\.org/ns/1\.0">\s*(<pb\s+n="18")', r'\1', content)
content = re.sub(r'</list>\s*</TEI>\s*(<pb\s+n="19")', r'</list>\n            \1', content)

# 2. Fix specific XML error on line 833 of unedited file (line 831 of edited file)
# The line is:
# lmŠkyl lBRK (1 Q Sb V, 20) also pN-pI.
# Let's replace this with italics for scroll name
content = content.replace('lmŠkyl lBRK (1 Q Sb V, 20) also pN-pI.', 'lmŠkyl lBRK (<hi rend="italic">1 Q Sb</hi> V, 20) also pN-pI.')

# 3. Normalize any pre-existing unstyled <hi> scroll refs
content = re.sub(r'<hi>\s*1\s*Q\s*S\s*:\s*</hi>', r'<hi rend="italic">1 Q S</hi>:', content)
content = re.sub(r'<hi>\s*1\s*Q\s*S\s*\n?\s*V,\s*</hi>', r'<hi rend="italic">1 Q S</hi> V,', content)

# Split by tags
tokens = re.split(r'(<[^>]+>)', content)
term_depth = 0
hi_depth = 0

# Lists of patterns to replace in text nodes
# 1. Scroll names
scrolls = ['1 Q Serek', '1 Q Milḥamah', '1 Q S', '1 Q M', '1 Q Sa', '1 Q Sb', '1 Q p Hab']

# 2. Hebrew phrases / terms
hebrew_phrases = [
    # Phrases
    "'WRKYH KWL H'DH",
    "'NW 'M QWDSKH",
    "HYWM MW'DW",
    "W['TH] 'L 'BWTYNW",
    "W'NW 'M [GWR]L[KH]",
    "wkly MLḤMWTM / HMH / MWR'M",
    "H'YŠ HNS'L / Y- / -DBR BTRW",
    "hdgl hmtqrb / kwlm / šB' m'rkwt",
    "hwnm",
    "wh'yš... yšlhhw",
    "wkwl hn'šh bw yršh bndbh",
    "kwl hb' ... / kwl 'yš mh mh... / y- /-šlhhw",
    "pšrw / hqryh / hy' / yrwšlm",
    "wl'wš byd rmh lw' yšwb 'wd",
    "wN’NŠ", "w’MD", "w’L HMQDŠ",
    "B'BR PWRT", "LW' BMḤYR", "KTWB",
    "'ŠR B'ŠT BYT 'ŠM[TMH] Y'BWRW",
    "M'Z",
    "w’šR ydbR bpyhw dbR nbl šlwšh ḥwdšYM",
    "HY'H 'T ... LMDBR",
    "WKN LNWQM LNPŠW KWL DBR",
    "LW' LHWKYḤ", "B'T HZW'T", "MKWL 'WL",
    "wlkwl gbwryhm 'yn m'md",
    "w'yn 'wzr lw", "w'yn sn'h",
    "wmN’[wryw ll]mdhw", "wl[qḥt]",
    "wlw’ lswr", "w’yn ls’wd", "wyhκyn pʿmyw",
    "wlw’ lnw, bkwḥkh, wb‘wz ḥylkh hgdwl",
    "wmwbdl",
    # Single words with boundaries
    "’ŠR", "’šR", "’ŠR", "’šR", "’xn", "’šn", "'ŠR", "šM", "ŠM", "šm",
    "YŠ", "yš", "ʔš", "sbyb", "hyh", "hw'h", "z'wm",
    "WKN", "KN", "HNH", "HMH", "HY'(H)", "HW'(H)", "HY'H",
    "’YH", "’WD", "'YH", "'WD", "KY'", "’L", "’NW", "’TH", "’BWTYNW",
    "w’šR", "w’yn", "w’yš", "lhBYn", "lbrk", "wllMD", "lBRK", "mwšly",
    "wbḥ", "šws", "rwt", "mry'ym", "lwyz'wm", "lmŠkyl", "mwhlḥ", "’lḥ",
    "ḥwqym", "drκym", "pʿmyw", "ȚRM", "TMYD", "HLWK", "HȚL"
]

# 3. Grammatical notation terms
grammatical_terms = [
    # Combinations
    "N-V", "N-N-V", "N-pt-V", "N-cN-cN-V",
    "pN-V", "pN-cpt-V", "pN-pN-V", "pN-cpN-V",
    "pI-V", "pI-pN-V", "pI-cV",
    "pt-V", "Ns-V", "Ns-pN-V", "Ns-pN-cpN-V", "Ns-pt-V",
    # Single ones
    "pN", "pI", "pt", "Ns", "N", "V"
]

# Strict boundary checking regex helper
def wrap_in_text(text, word, replacement):
    # Only replace if it's a whole word.
    # Word boundary checking using negative lookbehind and lookahead for letters/digits/diacritics/symbols
    pattern = rf'(?<![a-zA-Z\u0100-\u02AF\u1E00-\u1EFF\u0590-\u05FF0-9\-\[\]\'])' + re.escape(word) + rf'(?![a-zA-Z\u0100-\u02AF\u1E00-\u1EFF\u0590-\u05FF0-9\-\[\]\'])'
    return re.sub(pattern, replacement, text)

# Process tokens
for idx in range(len(tokens)):
    token = tokens[idx]
    if token.startswith('<'):
        # Update depth states
        if token.startswith('<term'):
            term_depth += 1
        elif token == '</term>':
            term_depth -= 1
        elif token.startswith('<hi'):
            hi_depth += 1
        elif token == '</hi>':
            hi_depth -= 1
    else:
        # It's a text node. Only edit if we are not already inside a <term>
        if term_depth == 0:
            # 1. Replace scroll references if not in <hi>
            if hi_depth == 0:
                for scroll in sorted(scrolls, key=len, reverse=True):
                    token = wrap_in_text(token, scroll, f'<hi rend="italic">{scroll}</hi>')
            
            # 2. Replace Hebrew terms/phrases
            for phrase in sorted(hebrew_phrases, key=len, reverse=True):
                token = wrap_in_text(token, phrase, f'<term xml:lang="hbo-Latn">{phrase}</term>')
                
            # 3. Replace grammatical terms
            for g_term in sorted(grammatical_terms, key=len, reverse=True):
                # Special handling for Ns/Ns references to avoid breaking superscript tags if we add them later,
                # but wait: we already normalized Ns/Ns to N<hi rend="sup">s</hi> or N<hi>s</hi> in some places.
                # Let's map Ns and Nˢ to N<hi rend="sup">s</hi> first, then wrap.
                token = wrap_in_text(token, g_term, f'<term xml:lang="hbo-Latn">{g_term}</term>')
            
            tokens[idx] = token

# Rebuild content
new_content = ''.join(tokens)

# Normalize superscript tags: e.g. Nˢ or Ns -> N<hi rend="sup">s</hi>
# Let's do this outside to be safe, but wait: if we wrapped Ns, it would be <term...>Ns</term>.
# We should change <term...>Ns</term> to <term...>N<hi rend="sup">s</hi></term>!
new_content = new_content.replace('Ns', 'N<hi rend="sup">s</hi>')
new_content = new_content.replace('Nˢ', 'N<hi rend="sup">s</hi>')
# Wait, let's make sure we also fix any nested term tags that might have slipped through
# (mismatched states or multiple regex match overlap)
# We can run our simple scanner on the rebuilt content!
output = []
depth = 0
rebuilt_tokens = re.split(r'(</?term(?: [^>]*)?>)', new_content)
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

final_content = ''.join(output)

print("Original terms:", new_content.count('<term'))
print("Final terms:", final_content.count('<term'))

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Formatting successfully completed.")
