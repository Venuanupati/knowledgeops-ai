# KnowledgeOps AI Demo Script

This demo shows how KnowledgeOps AI ingests documents, indexes them into a vector database, and answers questions using Retrieval-Augmented Generation.


## 1. Start the application

Run:
make up

Open:

http://localhost:8000/docs

## 2. Check API health

Call:
GET /api/v1/health

Expected result:
{
 "status": "ok",
 "postgres": "ok",
 "qdrant": "ok"
}

## 3. Upload a document

Call:
POST /api/v1/ingest

Upload a sample PDF, TXT, or DOCX file.

Expected result:
{
 "document_id": 1,
 "filename": "uuid_policy.pdf",
 "saved_path": "/app/data/raw/uuid_policy.pdf",
 "extracted_text_length": 8421,
 "chunks_created": 5,
 "message": "File uploaded, processed, stored, and indexed successfully."
}

Explaination:

the file was validated,
text was extracted,
chunks were created,
embeddings were generated,
vectors were stored in Qdrant,
metadata was stored in Postgres.

## 4. View uploaded documents

Call:
GET /api/v1/documents

Explaination:

documents are paginated,
each document has a status,
chunk_count confirms ingestion output.

## 5. Ask a question

Call:
POST /api/v1/chat

Example request:
{
 "question": "What is the leave policy?",
 "document_id": 1,
 "top_k": 5,
 "include_sources": true
}

Expected result:
{
 "chat_id": 1,
 "answer": "Employees are entitled to 15 paid leave days annually [SOURCE 1].",
 "confidence": "high",
 "sources": [
   {
     "document_id": 1,
     "chunk_id": 3,
     "filename": "uuid_policy.pdf",
     "chunk_index": 2,
     "score": 0.91,
     "snippet": "Employees are entitled to 15 paid leave days annually..."
   }
 ]
}

Explaination:

the question was embedded,
Qdrant retrieved relevant chunks,
a grounded prompt was built,
the LLM answered using retrieved context,
sources and confidence were returned.

## 6. Review chat history

Call:
GET /api/v1/chat-logs

Explaination:

previous questions and answers are stored,
sources are saved for auditability,
confidence is tracked.

## 7. Submit feedback

Call:
POST /api/v1/chat-feedback

Example request:
{
 "chat_id": 1,
 "rating": "up",
 "comment": "This answer was accurate and helpful."
}

Explaination:

user feedback is saved,
feedback can be used for future evaluation and prompt improvement.

## 8. View summaries

Call:
GET /api/v1/status
GET /api/v1/documents-summary
GET /api/v1/chat-summary
GET /api/v1/chat-feedback-summary

Explaination:

these endpoints support admin dashboards,
they give visibility into document ingestion, chat quality, and feedback trends.

## 9. Reindex a document

Call:
POST /api/v1/documents/{document_id}/reindex

Explaination:

reindexing supports updated chunking or embedding logic,
old vectors are deleted and recreated.

## 10. Delete a document

Call:
DELETE /api/v1/documents/{document_id}

Explaination:

metadata is removed from Postgres,
vectors are removed from Qdrant,
raw file is removed from local storage.

## Closing Explanation

KnowledgeOps AI demonstrates a production-style GenAI backend with:

document ingestion
RAG
vector databases
embeddings
APIs
metadata storage
feedback loops
observability
migrations
tests
CI/CD foundation

This project can be extended into a full enterprise knowledge assistant.


