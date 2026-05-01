from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model=settings.OPENAI_EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def generate_query_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model=settings.OPENAI_EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
