# KnowledgeOps AI

KnowledgeOps AI is a production-style GenAI knowledge assistant that can ingest documents, generate embeddings, store them in a vector database, and answer questions using Retrieval-Augmented Generation.

## Current Features

- FastAPI backend
- Docker-based local setup
- PostgreSQL metadata storage
- Qdrant vector database
- Document upload and ingestion
- PDF, TXT, and DOCX parsing
- Text chunking
- OpenAI embeddings
- RAG-based chat endpoint
- Source citations
- Chat history storage
- Feedback collection
- Document deletion and re-indexing
- Health checks for Postgres and Qdrant
- Pagination and filtering for admin APIs

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Qdrant
- OpenAI API
- Docker Compose

## Run Locally

docker compose -f infra/docker/docker-compose.yml up --build

## Database Migrations

This project uses Alembic for database migrations.

Check current migration:

make migrate-current

Create a new migration:

make migrate-new msg="your migration message"

Apply migrations:

make migrate-up

Note: For local Alembic commands, apps/api/.env may use localhost for DATABASE_URL, while Docker uses postgres

### Local Alembic Environment

For local Alembic commands, create a local environment file inside `apps/api`:

cp ../../.env .env

Then update the local database URL in apps/api/.env:

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/knowledgeops
POSTGRES_HOST=localhost

Docker services should continue using the root .env, where:

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/knowledgeops
POSTGRES_HOST=postgres

The file apps/api/.env is ignored by Git.

## API Docs

After starting the app, open:

http://localhost:8000/docs

## API Versioning

All application endpoints are available under:

/api/v1

Examples:
GET /api/v1/health
POST /api/v1/ingest
POST /api/v1/chat
GET /api/v1/documents

The root endpoint remains:

GET /

## Health Check

http://localhost:8000/health

## Environment Variables

Create a .env file in the project root and include:

APP_NAME=knowledgeops-ai
APP_ENV=local
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=knowledgeops
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/knowledgeops

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4.1-mini

QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=knowledge_chunks

TOP_K=5
MIN_TOP_K=1
MAX_TOP_K=10
MAX_UPLOAD_SIZE_MB=10
MIN_QUESTION_LENGTH=3
MAX_QUESTION_LENGTH=2000

Copy the example environment file:

cp .env.example .env

Then update OPENAI_API_KEY in .env.

## Architecture

See the full architecture document:

docs/ARCHITECTURE.md

## API Reference

See the API reference document:

docs/API_REFERENCE.md

## Roadmap

See the project roadmap:

docs/ROADMAP.md

## Demo Script

See the walkthrough demo script

docs/DEMO_SCRIPT.md

## Project Status

This project is currently under active development.


