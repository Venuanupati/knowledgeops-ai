from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.core.config import settings

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


def ensure_collection(vector_size: int) -> None:
    collections = client.get_collections().collections
    existing_names = [collection.name for collection in collections]

    if settings.QDRANT_COLLECTION not in existing_names:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def upsert_chunk_vector(
    chunk_id: int,
    embedding: list[float],
    document_id: int,
    filename: str,
    chunk_index: int,
    text: str,
) -> None:
    ensure_collection(vector_size=len(embedding))

    client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=[
            PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "chunk_id": chunk_id,
                    "filename": filename,
                    "chunk_index": chunk_index,
                    "text": text,
                },
            )
        ],
    )


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int,
    document_id: int | None = None,
) -> list[dict]:
    query_filter = None

    if document_id is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        )

    results = client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
        query_filter=query_filter,
    )

    points = results.points if hasattr(results, "points") else []

    matches = []
    for point in points:
        payload = point.payload or {}
        matches.append(
            {
                "document_id": payload.get("document_id"),
                "chunk_id": payload.get("chunk_id"),
                "filename": payload.get("filename"),
                "chunk_index": payload.get("chunk_index"),
                "text": payload.get("text"),
                "score": float(point.score) if getattr(point, "score", None) is not None else None,
            }
        )

    return matches


def delete_document_vectors(document_id: int) -> None:
    client.delete(
        collection_name=settings.QDRANT_COLLECTION,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        ),
    )
