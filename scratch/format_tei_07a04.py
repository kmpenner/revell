import re
import xml.etree.ElementTree as ET

xml_path = "/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/07a Articles/07a.04 - New Biblical Fragment/transcription_tei.xml"

with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean block footnotes (remove them completely using non-greedy DOTALL regexes)

# --- Note 5 ---
content = re.sub(r'<note xml:id="n5"[^>]*>.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<ptr target="#n5" />',
    '<note place="foot" n="5">In the first case the text is broken at the margin. The other two note the <hi rend="italic">qerê</hi> there. Cf. also the marginal note to 5: 6(?).</note>'
)

# --- Note 6 ---
content = re.sub(r'<note xml:id="n6"[^>]*>.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<ptr target="#n6" />',
    '<note place="foot" n="6">The bA form is noted as <hi rend="italic">kethîb</hi> in the margin.</note>'
)

# --- Note 7 ---
content = re.sub(r'<note xml:id="n7"[^>]*>.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(
    r'each case pointed, which suggests that the scribe pointed as he wrote\.\s*<ptr[^>]*>',
    'each case pointed, which suggests that the scribe pointed as he wrote.<note place="foot" n="7">The same is probably true of MdW II MS M, where a special form of <hi rend="italic">shin</hi> was written to accommodate internal points. This is not usually the case.</note>',
    content
)

# --- Note 8 ---
content = re.sub(r'<note xml:id="n8"[^>]*>.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<ptr target="#n8" />',
    '<note place="foot" n="8">As Dr. Dietrich has pointed out (<hi rend="italic">op. cit</hi>, 93), it is characteristic of Palestinian Biblical texts to show variants of the ‘vulgar text’ type.</note>'
)

# --- Note 9 ---
content = re.sub(r'<note xml:id="n9"[^>]*>.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<ptr target="#n9" />',
    '<note place="foot" n="9">The vocalisation of these fragments is described in greater detail in my book, <hi rend="italic">Hebrew Texts with Palestinian Vocalization</hi> (= HTPV) to be published by the University of Toronto Press.</note>'
)

# --- Note 15 ---
content = re.sub(r'<note n="15">See <hi rend="italic">HTPV</hi> IV\. 2, and V\.</note>', '', content)
# Correct inline note 15
content = re.sub(
    r'group B pointing\.<note n="15">(.*?)</note>',
    r'group B pointing.<note place="foot" n="15">See <hi rend="italic">HTPV</hi> IV. 2, and V.</note> \1',
    content,
    flags=re.DOTALL
)

# --- Note 22 ---
content = re.sub(r'<note n="22">22 <hi rend="italic">E\.g\.</hi>.*?</note>', '', content, flags=re.DOTALL)
# Correct inline note 22
content = re.sub(
    r'placed over those letters\.<note\s+n="22">(.*?)</note></p>',
    r'placed over those letters.<note place="foot" n="22"><hi rend="italic">E.g.</hi>, <seg xml:lang="he">תַּחַת (6: 22), וְאֵלֶּה (4: 3)</seg>.</note></p>\n            <p>\1</p>',
    content,
    flags=re.DOTALL
)

# --- Note 25 ---
content = re.sub(r'<note place="foot">\s*where, <hi rend="italic">e\.g\.</hi> MdW II MS J.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(
    r'is expected\.<note n="25" place="bottom">(.*?)</note>',
    r'is expected.<note place="foot" n="25">\1 where, <hi rend="italic">e.g.</hi> MdW II MS J, Dan. 11: 15, 16, 17, MS L, Ps. 70: 3 (the conjunction), Bodleian MS Heb. d41, f. 15r20, 13r29, 14r30 (<foreign xml:lang="heb">חחייח</foreign> and <foreign xml:lang="heb">חחיית</foreign> in an MS with two interchangeable ‘a’ signs). These MSS are all of group B. It is possible that Ḥayyuj’s emphasis on the rule that ‘Vocal <hi rend="italic">shewa</hi> before <hi rend="italic">yod</hi> is pronounced as <hi rend="italic">ḥireq</hi>’ was directed against similar pronunciations. See Nutt, J. W., Two Treatises... by R. Jehuda Ḥayug (London 1870) 131.</note>',
    content,
    flags=re.DOTALL
)

# --- Note 26 ---
content = re.sub(r'<note n="26" place="foot">\s*<foreign xml:lang="heb">ה</foreign>.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<note n="26" place="foot">See below.</note>',
    '<note place="foot" n="26"><foreign xml:lang="heb">ה</foreign> for <foreign xml:lang="heb">אהרן</foreign> could be explained, but not, I think, convincingly. It may be an error (cf. ר 5: 29). The same is likely for ר for מרים, unless the suggestion in 6.4 is correct.</note>'
)

# --- Note 27 ---
content = re.sub(r'<note n="27" place="foot">\s*<foreign xml:lang="heb">ר</foreign>.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<note n="27" place="foot">See below.</note>',
    '<note place="foot" n="27"><foreign xml:lang="heb">ר</foreign> for <foreign xml:lang="heb">גבר</foreign> (5: 2) might present a difficulty, but it too may be an error. Cf. form 8 of 5.3(iii) with 13 of 5.3(v).</note>'
)

# --- Note 28 ---
content = re.sub(r'<note n="28" place="foot">\s*<hi rend="italic">E\.g\.</hi>.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(
    r'<note n="28" place="foot">See\s+below\.</note>',
    '<note place="foot" n="28"><hi rend="italic">E.g.</hi>, <foreign xml:lang="heb">השיבו</foreign>, MdW II MS H, Ez. 14: 6, <foreign xml:lang="heb">יביאו</foreign> <hi rend="italic">ibid.</hi>, MS L, Ps. 69: 28, <foreign xml:lang="heb">השע</foreign> Murtonen, <hi rend="italic">op. cit.</hi>, MS c, Ps. 39: 14 (again all group B MSS). The ‘e’ signs almost certainly represent ‘shewa vowels’, see my “Studies in the Vocalization of Palestinian Hebrew” (to be published in a <hi rend="italic">Toronto Texts and Studies</hi> volume by the University of Toronto Press), No. 21 ff.</note>',
    content
)

# --- Note 29 ---
content = re.sub(r'<note n="29" place="foot">\s*Reasons for rejecting.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(r'<note place="foot">of Hebrew gradually.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<note n="29" place="foot">See below.</note>',
    '<note place="foot" n="29">Reasons for rejecting the view that the Palestinian pointing represents a pre-bA stage of Hebrew gradually brought under bA influence are given in my “Studies” (see note 28) especially No. 31 ff.</note>'
)

# --- Note 30 ---
content = re.sub(r'<note n="30" place="foot">Note also the conflicting.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(
    r'variation at all\.<note n="30">(.*?)</note></p>',
    r'variation at all.<note place="foot" n="30">Note also the conflicting forms listed in 5.3(v).</note> \1</p>',
    content,
    flags=re.DOTALL
)

# --- Note 31 ---
content = re.sub(r'<note n="31" place="foot">Dr\. Dietrich argues.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(
    r'form and position<note n="31">(.*?)</note>',
    r'form and position<note place="foot" n="31">Dr. Dietrich argues that it was bA influence which led to the placing of the Palestinian accent signs on the stress syllable (<hi rend="italic">op. cit.</hi> p. 109 f.). This cannot be maintained here. bA <hi rend="italic">pashta</hi>, <hi rend="italic">geresh</hi>, and <hi rend="italic">telisha</hi> obviously did not influence the position of the corresponding signs in this MS. In fact with <hi rend="italic">geresh</font> the reverse is true (see 4.2 x). It cannot be reasonably maintained that bA influence affected the positioning only of the other accent signs. The fact is that, although the number of ‘accents’ and their use appears to have been fairly stable, the history of the means of representing them is complex. Various systems were used, both with Palestinian and with Tiberian vowel signs, and, as with the vowel signs, the idea of a single stream of evolution from Palestinian to bA does not satisfy the facts.</note> \1',
    content,
    flags=re.DOTALL
)

# --- Note 32 ---
content = re.sub(r'<note n="32" place="foot">These systems are found.*?</note>', '', content, flags=re.DOTALL)
content = re.sub(
    r'Palestinian MSS are<note n="32">(.*?)</note>',
    r'Palestinian MSS are<note place="foot" n="32">These systems are found as follows:— 1, <hi rend="italic">e.g.</hi> Bod. Heb. d29, f. 17–20 (Dietrich, <hi rend="italic">op. cit.</hi> MS Ob 1); 2, <hi rend="italic">e.g.</hi> MdW II, MS J; 3, <hi rend="italic">ibid.</hi> MS M; 4, <hi rend="italic">ibid.</font> MS K, and TS NS 246:22 (Diez Macho, <hi rend="italic">Studia Papyrologica</font> VI, 1967, p. 15–25). There is some variation in the sign use shown in the table in systems 3 and 4.</note>\1',
    content,
    flags=re.DOTALL
)

# --- Note 36 ---
content = re.sub(r'<note n="36" xml:id="n36">.*?</note>', '', content, flags=re.DOTALL)
content = content.replace(
    '<ptr target="#n36" />',
    '<note place="foot" n="36">See Dietrich, <hi rend="italic">op. cit.</hi>, 109 f.</note>'
)

# 2. Normalize simple inline notes to <note place="foot" n="XX">
def normalize_simple_notes(match):
    attrs = match.group(1)
    num_match = re.search(r'n="(\d+)"', attrs)
    if num_match:
        n = num_match.group(1)
        return f'<note place="foot" n="{n}">'
    return match.group(0)

content = re.sub(r'<note ([^>]*n="\d+"[^>]*)>', normalize_simple_notes, content)

# 3. Standardize running headers to <fw type="header" place="top">...</fw>
content = re.sub(
    r'<head>E\.\s*J\.\s*REVELL</head>',
    '<fw type="header" place="top">E. J. REVELL</fw>',
    content,
    flags=re.IGNORECASE
)
content = re.sub(
    r'<head>A\s+NEW\s+BIBLICAL\s+FRAGMENT</head>',
    '<fw type="header" place="top">A NEW BIBLICAL FRAGMENT</fw>',
    content,
    flags=re.IGNORECASE
)
content = re.sub(
    r'<head>A\s+NEW\s+BIBLICAL\s+FRAGMENT\s+67</head>',
    '<fw type="header" place="top">A NEW BIBLICAL FRAGMENT 67</fw>',
    content,
    flags=re.IGNORECASE
)
content = re.sub(
    r'<fw type="header" rend="align\(center\)">\s*66\s*<space quantity="20" unit="character" />\s*E\.\s*J\.\s*REVELL\s*</fw>',
    '<fw type="header" place="top">66 E. J. REVELL</fw>',
    content,
    flags=re.IGNORECASE
)
content = re.sub(
    r'<list>\s*<item>68</item>\s*<item>E\.\s*J\.\s*REVELL</item>\s*</list>',
    '<fw type="header" place="top">68 E. J. REVELL</fw>',
    content,
    flags=re.IGNORECASE
)
content = re.sub(
    r'<head>72\s+E\.\s*J\.\s*REVELL</head>',
    '<fw type="header" place="top">72 E. J. REVELL</fw>',
    content,
    flags=re.IGNORECASE
)
content = re.sub(
    r'<head>A\s+NEW\s+BIBLICAL\s+FRAGMENT\s+<fw type="pageNum">73</fw></head>',
    '<fw type="header" place="top">A NEW BIBLICAL FRAGMENT 73</fw>',
    content,
    flags=re.IGNORECASE
)

# 4. Standardize font tags to hi
content = content.replace("</font>", "</hi>")

# Let's write the modified XML back to file
with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Modification complete. Attempting to parse the resulting XML...")
try:
    ET.fromstring(content)
    print("Success! The XML is well-formed.")
except Exception as e:
    print(f"Error: The resulting XML is NOT well-formed: {e}")
