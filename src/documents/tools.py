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
    """Load a PDF file and return a list of Documents."""
    return load_pdf(path)

@tool("load_txt_tool")
def load_txt_tool(path: str) -> List[Document]:
    """Load a TXT file and return a list of Documents."""
    return load_txt(path)

@tool("load_markdown_tool")
def load_markdown_tool(path: str) -> List[Document]:
    """Load a Markdown file and return a list of Documents."""
    return load_markdown(path)

# === CLEANING ===

@tool("clean_text_tool")
def clean_text_tool(text: str) -> str:
    """Clean the input text and return the cleaned version."""
    return clean_text(text)

# === SPLITTING ===

@tool("split_texts_tool")
def split_texts_tool(input_data: Dict[str, List[Document]]) -> List[Document]:
    """Split documents into smaller chunks with token and sentence overlap."""
    docs = input_data["docs"]
    return split_documents(docs, max_tokens=600, overlap_sentences=2)

# === SIMPLE SEARCH ===

DOC_STORE: List[Document] = [] 

@tool("set_corpus_tool")
def set_corpus_tool(input_data: Dict[str, List[Document]]) -> str:
    """Set the global document corpus for keyword search."""
    global DOC_STORE
    docs = input_data["docs"]
    DOC_STORE = docs
    return f"Corpus initialized with {len(docs)} documents."

@tool("search_keyword_tool")
def search_keyword_tool(query: str) -> List[str]:
    """Search the global document corpus for keywords and return top results."""
    return keyword_search(DOC_STORE, query, k=3)