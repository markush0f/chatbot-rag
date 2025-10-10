from app.utils.chunker import split_text_by_tokens
import pytest


def test_split_basic():
    text = " ".join(["palabra"] * 1000)  # texto con 1000 palabras
    chunks = split_text_by_tokens(text, chunk_size=100, overlap=10)
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)
    assert any("palabra" in c for c in chunks)
    assert chunks[0] != chunks[-1]  # deberían ser diferentes


def test_empty_text():
    assert split_text_by_tokens("") == []
    assert split_text_by_tokens("   ") == []


def test_overlap_behavior():
    text = " ".join(["token"] * 300)
    chunks = split_text_by_tokens(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    # Los chunks deben tener solapamiento (palabras repetidas entre ellos)
    overlap_found = any(word in chunks[i + 1] for i, word in enumerate(chunks[:-1]))
    assert overlap_found


def test_respects_token_limit():
    text = " ".join(["data"] * 1200)
    chunks = split_text_by_tokens(text, chunk_size=256, overlap=32)
    assert all(len(c.split()) <= 300 for c in chunks)  # aprox por palabras
