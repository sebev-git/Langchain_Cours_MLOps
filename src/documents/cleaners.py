import re

def clean_text(text: str) -> str:
    if not text or text.strip() == "":
        return ""

    # Remove isolated page numbers
    text = re.sub(r'^\s<i>\d+\s</i>$', '', text, flags=re.MULTILINE)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()