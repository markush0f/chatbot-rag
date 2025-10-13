"""
prompts.py
----------
Prompt templates for chat and RAG generation.
"""


def rag_prompt(context: str, question: str) -> str:
    """Generate a structured prompt for RAG-based question answering."""
    return f"""
    You are a helpful assistant that answers questions based only on the following context.

    Context:
    {context}

    Question:
    {question}

    Respond concisely and factually, using only information from the context.
    If the answer is not in the context, respond with "I don't have that information in the provided documents."
    """
