from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "knowledgeops-ai"
    APP_ENV: str = "local"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "knowledgeops"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/knowledgeops"

    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_CHAT_MODEL: str = "gpt-4.1-mini"

    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "knowledge_chunks"

    TOP_K: int = 5
    MIN_TOP_K: int = 1
    MAX_TOP_K: int = 10
    MAX_UPLOAD_SIZE_MB: int = 10
    MIN_QUESTION_LENGTH: int = 3
    MAX_QUESTION_LENGTH: int = 2000

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
