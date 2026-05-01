# KnowledgeOps AI 🚀

A production-style GenAI backend system for document ingestion, vector search, and Retrieval-Augmented Generation (RAG) with source citations, confidence scoring, and feedback loops.

---

## 🔥 Key Features
- 📄 Document ingestion (PDF, TXT, DOCX)
- ✂️ Intelligent text chunking
- 🔎 Vector search using Qdrant
- 🤖 RAG-based question answering
- 📚 Source citations with confidence scoring
- 🧠 Feedback loop for response evaluation
- 📊 Admin APIs (documents, chats, feedback)
- ⚙️ Production-ready backend (FastAPI + PostgreSQL)
- 🧪 Full test suite (pytest + coverage + CI)
- 🛠️ Alembic migrations + DB lifecycle management

---

## 🏗️ Architecture Overview
User → FastAPI → RAG Pipeline → Qdrant (Vector DB)
 ↓
 PostgreSQL (Metadata)

Detailed architecture:
docs/ARCHITECTURE.md

---

## ⚡ Quick Start
git clone <your-repo>
cd knowledgeops-ai

cp .env.example .env
--> Add your OPENAI_API_KEY

make up

Open:
http://localhost:8000/docs

## 📡 API Highlights
POST /api/v1/ingest → Upload & index documents
POST /api/v1/chat → Ask questions (RAG)
GET /api/v1/documents → List documents
GET /api/v1/chat-logs → View chat history
POST /api/v1/chat-feedback → Submit feedback

Full reference:
docs/API_REFERENCE.md

## 🤖 RAG Flow
User Question
   ↓
Embedding (OpenAI)
   ↓
Vector Search (Qdrant)
   ↓
Top-K Chunks Retrieved
   ↓
LLM Prompt Construction
   ↓
Answer + Sources + Confidence

## 📄 Document Ingestion Flow
Upload → Validate → Extract → Chunk → Embed → Store → Index

## 🧪 Testing
Run all tests:
make test-api

Run unit tests:
make test-unit

Run integration tests:
make test-integration

Run coverage:
make test-api-cov

## 🛠️ Tech Stack
FastAPI
PostgreSQL
Qdrant (Vector DB)
OpenAI (Embeddings + LLM)
Docker
Alembic
Pytest
Ruff
GitHub Actions

## 🗂️ Project Docs
Architecture → docs/ARCHITECTURE.md
API Reference → docs/API_REFERENCE.md
Roadmap → docs/ROADMAP.md
Demo Script → docs/DEMO_SCRIPT.md

## 💾 Database Migrations
make migrate-current
make migrate-new msg="your migration"
make migrate-up

## 🧠 Why This Project Matters
This project demonstrates:
End-to-end GenAI system design
Production-style backend engineering
RAG pipeline implementation
Vector database usage
API design + observability
Testing + CI/CD practices

## 🚀 Future Improvements
Hybrid search (BM25 + vector)
Reranking models
Frontend UI (React)
Async ingestion pipeline
Evaluation framework (MLflow)

## 📸 Demo
(Will add Snaps in comming days)

# 📌 Status
Currently under active development