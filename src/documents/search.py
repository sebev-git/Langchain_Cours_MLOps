import re
from typing import List
from langchain_core.documents import Document

def keyword_search(docs: List[Document], query: str, k: int = 3) -> List[str]:
    results = []
    query_lower = query.lower()

    for doc in docs:
        text = doc.page_content
        if query_lower in text.lower():
            match = re.search(query, text, re.IGNORECASE)
            if match:
                start = max(0, match.start() - 150)
                end = min(len(text), match.end() + 150)
                snippet = text[start:end]
                results.append(snippet)

    return results[:k] if results else ["No results found."]