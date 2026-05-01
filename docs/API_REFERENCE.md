# KnowledgeOps AI API Reference

## Base URL:

http://localhost:8000/api/v1

## Health

GET /ping

Lightweight liveness check.

Response:
{
 "status": "ok"
}

GET /health

Checks API dependency health.

Response:
{
 "status": "ok",
 "postgres": "ok",
 "qdrant": "ok"
}

GET /info

Returns API metadata.

GET /status

Returns system-level counts.

## Documents

POST /ingest

Uploads and indexes a document.

Supported file types:
.pdf
.txt
.docx

Response:
{
 "document_id": 1,
 "filename": "uuid_policy.pdf",
 "saved_path": "/app/data/raw/uuid_policy.pdf",
 "extracted_text_length": 8421,
 "chunks_created": 5,
 "message": "File uploaded, processed, stored, and indexed successfully."
}

GET /documents

Lists documents.

Query parameters:

Parameter                Type                Description
status                   string              Optional filter: uploaded, chunked, indexed
limit                    integer             Page size
offset                   integer             Page offset

Response:
{
 "items": [],
 "total": 0,
 "limit": 20,
 "offset": 0
}

GET /documents/{document_id}

Returns document metadata.

GET /documents/{document_id}/chunks

Returns chunks for a document.

Query parameters:

Parameter                Type                Description
include_full_text        boolean             Whether to return full chunk text
limit                    integer             Page size
offset                   integer             Page offset

DELETE /documents/{document_id}

Deletes a document, its chunks, vectors, and stored file.

POST /documents/{document_id}/reindex

Re-indexes an existing document.

GET /documents-summary

Returns document count summary.

## Chat

POST /chat

Runs a RAG question-answering request.

Request:
{
 "question": "What is the leave policy?",
 "document_id": 1,
 "top_k": 5,
 "include_sources": true
}

Fields:

Field                Type                Required                Description
question             string              Yes                     User question
document_id          integer             No                      Restrict retrieval to one document
top_k                integer             No                      Number of chunks to retrieve
include_sources      boolean             No                      Whether to return sources

Response:
{
 "chat_id": 1,
 "answer": "Employees are entitled to 15 paid leave days annually [SOURCE 1].",
 "confidence": "high",
 "sources": [
   {
     "document_id": 1,
     "chunk_id": 3,
     "filename": "employee_handbook.pdf",
     "chunk_index": 2,
     "score": 0.91,
     "snippet": "Employees are entitled to 15 paid leave days annually..."
   }
 ]
}

GET /chat-logs

Lists chat logs.

Query parameters:

Parameter                Type                Description
chat_id                  integer             Optional chat ID filter
confidence               string              Optional filter: high, medium, low
include_full_text        boolean             Whether to return source full text
limit                    integer             Page size
offset                   integer             Page offset

GET /chat-logs/{chat_id}

Returns one chat log.

GET /chat-summary

Returns chat confidence summary.

## Feedback

POST /chat-feedback

Submits feedback for a chat response.

Request:
{
 "chat_id": 1,
 "rating": "up",
 "comment": "Helpful answer."
}

Allowed ratings:
up
down

Response:
{
 "feedback_id": 1,
 "chat_id": 1,
 "rating": "up",
 "comment": "Helpful answer.",
 "message": "Feedback submitted successfully."
}

GET /chat-feedback

Lists feedback.

Query parameters:

Parameter                Type                Description
chat_id                  integer             Optional chat ID filter
rating                   string              Optional filter: up, down
limit                    integer             Page size
offset                   integer             Page offset

GET /chat-feedback/{feedback_id}

Returns one feedback record.

GET /chat-feedback-summary

Returns feedback summary.

## Debug

GET /debug-error

Raises an intentional error for local error-handler testing.

Only available when:
APP_ENV=local