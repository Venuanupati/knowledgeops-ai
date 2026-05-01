from typing import List


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 300) -> List[str]:
    """
    Split text into overlapping character-based chunks.
    """
    if not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
