import tiktoken
from typing import List


def split_text_by_tokens(
    text: str,
    model_name: str = "text-embedding-3-small",
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[str]:
    """
    Split text into overlapping chunks based on token count, using tiktoken.
    Args:
        text (str): _description_
        model_name (str, optional): _description_. Defaults to "text-embedding-3-small".
        chunk_size (int, optional): _description_. Defaults to 500.
        overlap (int, optional): _description_. Defaults to 50.

    Returns:
        List[str]: List of text chunks (decoded back to strings).
    """

    if not text or not text.strip():
        return []

    # Load encoder compatible with the embedding model
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    total_tokens = len(tokens)

    if total_tokens == 0:
        return []

    chunks = []
    start = 0

    while start < total_tokens:
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens).strip()
        if chunk_text:
            chunks.append(chunk_text)
        start += chunk_size - overlap
        
    return chunks
