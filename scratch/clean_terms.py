import re

file_path = '07a Articles/07a.02 - Clause Structure Prose/transcription_tei.xml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's write a robust parser to find nested <term> elements and flatten them.
# A simple way to do this with regex or string replacement is to match inner <term xml:lang="hbo-Latn">...</term>
# when they are already inside another <term xml:lang="hbo-Latn">...</term>.
# Since the outer tag has <term xml:lang="hbo-Latn"> and closing </term>, we can find them.
# Let's use re.finditer to locate all term blocks and check if they overlap or nest.

def flatten_nested_terms(text):
    # We can recursively remove nested <term...> and </term> tags.
    # To do this safely, we search for:
    # <term xml:lang="hbo-Latn">(.*?)<term xml:lang="hbo-Latn">(.*?)</term>(.*?)</term>
    # and replace with:
    # <term xml:lang="hbo-Latn">\1\2\3</term>
    # We do this in a loop until no more changes are made.
    pattern = r'(<term xml:lang="hbo-Latn">[^<]*?)<term xml:lang="hbo-Latn">([^<]*?)</term>([^<]*?</term>)'
    
    modified = True
    while modified:
        text, count = re.subn(pattern, r'\1\2\3', text)
        if count == 0:
            modified = False
            
    # Also handle multiple nestings or spacing:
    # Let's do a general regex if needed, but the loop with subn is very safe.
    return text

cleaned_content = flatten_nested_terms(content)

# Let's check if the count of term tags has decreased
orig_count = content.count('<term')
new_count = cleaned_content.count('<term')
print(f"Original term count: {orig_count}, cleaned term count: {new_count}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print("Terms cleaned successfully.")
