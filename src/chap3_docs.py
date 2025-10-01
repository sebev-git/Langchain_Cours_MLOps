import os, random
from src.documents.loaders import load_pdf
from src.documents.cleaners import clean_text
from src.documents.splitters import split_documents
from src.documents.search import keyword_search
from src.utils.token import count_tokens

print("\n=== Full demo of document processing functions ===\n")
# --- 1. Random selection of a PDF ---
pdf_dir = "data/pdf"
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if not pdf_files:
    raise FileNotFoundError("No PDF found in data/pdf!")

pdf_path = os.path.join(pdf_dir, random.choice(pdf_files))
print(f"📄 Selected file: {pdf_path}")

# --- 2. Load the PDF ---
docs = load_pdf(pdf_path)
print(f"✅ PDF loaded: {len(docs)} pages")

# --- 3. Clean the content of each page ---
for d in docs:
    d.page_content = clean_text(d.page_content)
print("✅ Cleaning done")

# --- 4. Split into chunks of 600 tokens ---
chunks = split_documents(docs, max_tokens=600, overlap_sentences=2)
print(f"✅ Split into {len(chunks)} chunks (~600 tokens each)")

# --- 5. Run a simple search ---
query = "John McCarthy"
results = keyword_search(chunks, query, k=3)

print(f"\n🔍 Results for query: {query}\n")
for i, r in enumerate(results, 1):
    print(f"--- Result {i} ---\n{r}\n")

# --- 6. Check the size of the first chunks ---
print("\n=== Preview of the first chunks ===")
for i, c in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ({count_tokens(c.page_content)} tokens) ---")
    print(c.page_content)