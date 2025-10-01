from typing import List, Dict
from langchain_core.documents import Document
from langchain.tools import tool
from .loaders import load_pdf, load_txt, load_markdown
from .cleaners import clean_text
from .splitters import split_documents
from .search import keyword_search

# === LOADING ===

@tool("load_pdf_tool")
def load_pdf_tool(path: str) -> List[Document]:
    """Load a PDF and return a list of Documents (one per page)."""
    return load_pdf(path)

@tool("load_txt_tool")
def load_txt_tool(path: str) -> List[Document]:
    """Load a plain text file and return it as a Document."""
    return load_txt(path)

@tool("load_markdown_tool")
def load_markdown_tool(path: str) -> List[Document]:
    """Load a Markdown file and return it as a Document."""
    return load_markdown(path)

# === CLEANING ===

@tool("clean_text_tool")
def clean_text_tool(text: str) -> str:
    """Cleans up text by removing noise (page numbers, multiple spaces, etc.)."""
    return clean_text(text)

# === SPLITTING ===

@tool("split_texts_tool")
def split_texts_tool(input_data: Dict[str, List[Document]]) -> List[Document]:
    """Split documents into overlapping chunks for analysis by LLM."""
    docs = input_data["docs"]
    return split_documents(docs, max_tokens=600, overlap_sentences=2)

# === SIMPLE SEARCH ===

DOC_STORE: List[Document] = [] 

@tool("set_corpus_tool")
def set_corpus_tool(input_data: Dict[str, List[Document]]) -> str:
    """Saves a list of documents as a global corpus for future searches."""
    global DOC_STORE
    docs = input_data["docs"]
    DOC_STORE = docs
    return f"Corpus initialized with {len(docs)} documents."

@tool("search_keyword_tool")
def search_keyword_tool(query: str) -> List[str]:
    """Searches for a keyword in the current corpus and returns the corresponding excerpts."""
    return keyword_search(DOC_STORE, query, k=3)