import re

class Markdown:
    def __init__(self, extensions=None):
        self.Meta = {}
        
    def convert(self, text):
        self.Meta = {}
        # Simple front matter parser
        if text.startswith("---"):
            end_fm = text.find("---", 3)
            if end_fm != -1:
                fm_text = text[3:end_fm]
                for line in fm_text.splitlines():
                    if ":" in line:
                        parts = line.split(":", 1)
                        key = parts[0].strip()
                        val = parts[1].strip().strip('"').strip("'")
                        self.Meta[key] = [val]
                return text[end_fm+3:].strip()
        return text

def Markdown_func(extensions=None):
    return Markdown(extensions)

# Expose Markdown class
Markdown = Markdown
