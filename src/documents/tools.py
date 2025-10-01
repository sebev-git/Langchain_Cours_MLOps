from typing import List, Dict
from langchain_core.documents import Document
from langchain.tools import tool
from .loaders import load_pdf, load_txt, load_markdown
from .cleaners import clean_text
from .splitters import split_documents
from .search import keyword_search

# === CHARGEMENT ===

@tool("load_pdf_tool")
def load_pdf_tool(path: str) -> List[Document]:
    """Charge un fichier PDF depuis un chemin donné et retourne une liste de Documents LangChain."""
    return load_pdf(path)


@tool("load_txt_tool")
def load_txt_tool(path: str) -> List[Document]:
    """Charge un fichier texte brut et retourne une liste de Documents LangChain."""
    return load_txt(path)


@tool("load_markdown_tool")
def load_markdown_tool(path: str) -> List[Document]:
    """Charge un fichier Markdown et retourne une liste de Documents LangChain."""
    return load_markdown(path)


@tool("clean_text_tool")
def clean_text_tool(text: str) -> str:
    """Nettoie un texte en supprimant le bruit (numéros de page, espaces multiples, etc.)."""
    return clean_text(text)

DOC_STORE: List[Document] = [] 

@tool("split_texts_tool")
def split_texts_tool(input_data: Dict[str, List[Document]]) -> List[Document]:
    """Découpe les documents en chunks avec chevauchement, pour l’analyse par LLM."""
    docs = input_data["docs"]
    return split_documents(docs, max_tokens=600, overlap_sentences=2)


@tool("set_corpus_tool")
def set_corpus_tool(input_data: Dict[str, List[Document]]) -> str:
    """Enregistre une liste de Documents comme corpus global pour les recherches ultérieures."""
    global DOC_STORE
    docs = input_data["docs"]
    DOC_STORE = docs
    return f"Corpus initialisé avec {len(docs)} documents."


@tool("search_keyword_tool")
def search_keyword_tool(query: str) -> List[str]:
    """Searches for a keyword in the current corpus and returns the corresponding excerpts."""
    return keyword_search(DOC_STORE, query, k=3)

