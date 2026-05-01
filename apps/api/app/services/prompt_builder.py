def build_rag_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for idx, chunk in enumerate(retrieved_chunks, start=1):
        context_blocks.append(
            (f"[SOURCE {idx}] filename={chunk['filename']} chunk_index={chunk['chunk_index']}\n{chunk['text']}")
        )

    context = "\n\n".join(context_blocks)

    return f"""
You are a knowledge assistant answering questions only from the provided context.

Rules:
1. Answer only using the provided context.
2. If the answer is not in the context, say: "I could not find that in the provided documents."
3. Be concise and accurate.
4. Cite the supporting sources in your answer using labels like [SOURCE 1], [SOURCE 2].

Question:
{question}

Context:
{context}
""".strip()
