import logging
import time

from openai import OpenAI

from app.core.config import settings
from app.services.embedding_service import generate_query_embedding
from app.services.prompt_builder import build_rag_prompt
from app.services.vector_store import search_similar_chunks

client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)


def _calculate_confidence(retrieved_chunks: list[dict]) -> str:
    if not retrieved_chunks:
        return "low"

    scores = [chunk["score"] for chunk in retrieved_chunks if chunk.get("score") is not None]

    if not scores:
        return "medium"

    avg_score = sum(scores) / len(scores)
    top_score = max(scores)

    logger.info("Average retrieval score=%.4f, top score=%.4f", avg_score, top_score)

    if top_score >= 0.35 and avg_score >= 0.25:
        return "high"
    if top_score >= 0.20:
        return "medium"
    return "low"


def answer_question(
    question: str,
    document_id: int | None = None,
    top_k: int | None = None,
) -> tuple[str, list[dict], str]:
    logger.info("Received chat question: %s", question)

    if document_id is not None:
        logger.info("Applying document filter: document_id=%s", document_id)

    effective_top_k = top_k if top_k is not None else settings.TOP_K
    logger.info("Using top_k=%s for retrieval", effective_top_k)

    retrieval_start = time.perf_counter()

    query_embedding = generate_query_embedding(question)

    retrieved_chunks = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=effective_top_k,
        document_id=document_id,
    )

    retrieval_duration = time.perf_counter() - retrieval_start
    logger.info("Retrieval completed in %.3f seconds", retrieval_duration)
    logger.info("Retrieved %s chunks for question", len(retrieved_chunks))

    confidence = _calculate_confidence(retrieved_chunks)
    logger.info("Calculated confidence=%s", confidence)

    if not retrieved_chunks:
        logger.warning("No chunks retrieved for question")
        return "I could not find that in the provided documents.", [], confidence

    if confidence == "low":
        logger.warning("Low-confidence retrieval detected. Returning fallback without LLM generation.")
        return (
            "I could not confidently answer that from the provided documents. "
            "Try asking a more specific question or select the correct document.",
            retrieved_chunks,
            confidence,
        )

    prompt = build_rag_prompt(question, retrieved_chunks)

    generation_start = time.perf_counter()

    response = client.responses.create(
        model=settings.OPENAI_CHAT_MODEL,
        input=prompt,
    )

    generation_duration = time.perf_counter() - generation_start
    logger.info("Generation completed in %.3f seconds", generation_duration)

    answer_text = response.output_text.strip()
    logger.info("Generated answer successfully")

    return answer_text, retrieved_chunks, confidence
