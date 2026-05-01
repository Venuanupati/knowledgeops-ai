# KnowledgeOps AI Architecture

KnowledgeOps AI is a production-style GenAI backend for document ingestion, vector indexing, Retrieval-Augmented Generation, chat history, feedback collection, and admin operations.

## High-Level Architecture

User / Client
   |
   v
FastAPI Backend
   |
   |-- Document Ingestion
   |     |-- File validation
   |     |-- File storage
   |     |-- Text extraction
   |     |-- Chunking
   |     |-- Embedding generation
   |     |-- Vector indexing
   |
   |-- RAG Chat
   |     |-- Question validation
   |     |-- Query embedding
   |     |-- Qdrant retrieval
   |     |-- Prompt construction
   |     |-- LLM response generation
   |     |-- Source citation formatting
   |
   |-- Admin APIs
   |     |-- Document listing
   |     |-- Document detail
   |     |-- Chunk inspection
   |     |-- Reindexing
   |     |-- Deletion
   |
   |-- Feedback APIs
   |     |-- Submit feedback
   |     |-- Review feedback
   |     |-- Feedback summaries
   |
   |-- Observability
         |-- Request logging
         |-- Request IDs
         |-- Timing logs
         |-- Health checks

## Main Components

### FastAPI API Layer

The API layer exposes versioned endpoints under:
/api/v1

Key endpoint groups:
Health
Documents
Chat
Feedback
Summaries
Debug

### PostgreSQL

PostgreSQL stores structured metadata:
documents
document chunks
chat logs
chat feedback

### Qdrant

Qdrant stores vector embeddings for document chunks.

Each vector payload includes:
document ID
chunk ID
filename
chunk index
chunk text

### OpenAI

OpenAI is used for:
document chunk embeddings
query embeddings
LLM response generation

### RAG Flow

User question
   |
   v
Validate question
   |
   v
Generate query embedding
   |
   v
Search Qdrant
   |
   v
Retrieve top matching chunks
   |
   v
Build grounded prompt
   |
   v
Generate answer with LLM
   |
   v
Return answer + confidence + sources

### Ingestion Flow

Upload document
   |
   v
Validate file type and size
   |
   v
Save raw file
   |
   v
Extract text
   |
   v
Chunk text
   |
   v
Store document metadata in Postgres
   |
   v
Store chunks in Postgres
   |
   v
Generate embeddings
   |
   v
Store vectors in Qdrant
   |
   v
Mark document as indexed

## Database Tables

### documents

Stores document metadata.

### document_chunks

Stores chunk text and chunk index per document.

### chat_logs

Stores user questions, generated answers, confidence, and source JSON.

### chat_feedback

Stores user feedback for chat responses.

## Production-Style Features

This project includes:
API versioning
request IDs
global request logging
health checks for Postgres and Qdrant
Alembic database migrations
database backup and restore commands
pagination
filtering
response shaping
test suite
coverage reporting
CI workflow
linting and formatting
pre-commit hooks

## Local Development Services

The local Docker setup runs:
FastAPI API
PostgreSQL
Qdrant

## Future Improvements

Planned production improvements:
frontend application
authentication and RBAC
background workers for ingestion
hybrid search
reranking
prompt versioning
evaluation datasets
MLflow-based GenAI evaluation
tracing and metrics dashboard
deployment to cloud infrastructure