from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, TextLoader

def load_pdf(path: str):
    """Load a PDF and return a list of Documents (one per page)."""
    loader = PyPDFLoader(path)
    return loader.load()

def load_web(url: str):
    """Load the content of a web page."""
    loader = WebBaseLoader(url)
    return loader.load()

def load_txt(path: str, encoding: str = "utf-8"):
    """Load a plain text file (.txt)."""
    loader = TextLoader(path, encoding=encoding)
    return loader.load()

def load_markdown(path: str, encoding: str = "utf-8"):
    """Load a Markdown file (.md)."""
    return load_txt(path, encoding=encoding)