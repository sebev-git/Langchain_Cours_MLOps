from langchain_core.documents import Document
import re
from src.utils.token import count_tokens

def add_overlap(prev_chunk: str, next_chunk: str, num_sentences: int = 2) -> str:
    prev_sentences = re.split(r'(?<=[.!?])\s+', prev_chunk.strip())
    overlap_sentences = prev_sentences[-num_sentences:] if len(prev_sentences) >= num_sentences else prev_sentences
    return " ".join(overlap_sentences) + " " + next_chunk


def split_documents(documents, max_tokens: int = 600, overlap_sentences: int = 2):
    if not documents:
        return []

    final_chunks = []

    # Merge all pages into a single text
    full_text = " ".join(doc.page_content for doc in documents)
    metadata = documents[0].metadata

    # Split into sentences
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', full_text) if s.strip()]

    current_chunk, current_tokens, prev_chunk = [], 0, None

    for sentence in sentences:
        sent_tokens = count_tokens(sentence)

        if current_tokens + sent_tokens > max_tokens and current_chunk:
            chunk_text = " ".join(current_chunk)

            # Apply overlap if a previous chunk exists
            chunk_text = add_overlap(prev_chunk, chunk_text, overlap_sentences) if prev_chunk else chunk_text

            final_chunks.append(Document(page_content=chunk_text.strip(), metadata=metadata))

            prev_chunk, current_chunk, current_tokens = chunk_text, [sentence], sent_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sent_tokens

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunk_text = add_overlap(prev_chunk, chunk_text, overlap_sentences) if prev_chunk else chunk_text
        final_chunks.append(Document(page_content=chunk_text.strip(), metadata=metadata))

    return final_chunks