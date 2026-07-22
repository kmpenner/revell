import re

file_path = '07a Articles/07a.02 - Clause Structure Prose/transcription_tei.xml'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's clean the footnote block using a very simple, flexible regex
# We locate:
# <note place="foot" n="30"> ... </note> ... first note 31 ... second note 31 ...
# Let's search for note 30 and note 31 using a loose regex pattern that matches the broken section:
pattern = r'<note\s+place="foot"\s+n="30">.*?</note>\s*<note\s+place="foot"\s+n="31">.*?</note></hi>\s*I,\s*13,\s*one\s*in\s*<hi>\s*1\s*Q\s*S\s*</hi>\s*III,\s*26\.\s*</p>\s*</note>\s*<note\s+place="foot"\s+n="31">.*?</note>'

# Let's use re.DOTALL to match across newlines
match = re.search(pattern, content, re.DOTALL)
if match:
    print("Matched broken footnote block!")
    print(match.group(0))
else:
    print("Could not match broken footnote block!")
