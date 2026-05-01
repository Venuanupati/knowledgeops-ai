import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_document_detail_not_found():
    response = client.get("/api/v1/documents/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def test_document_chunks_not_found():
    response = client.get("/api/v1/documents/999999/chunks")

    assert response.status_code == 404
    assert response.json()["detail"] == "No chunks found for this document."


def test_chat_log_detail_not_found():
    response = client.get("/api/v1/chat-logs/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat log not found."


def test_feedback_detail_not_found():
    response = client.get("/api/v1/chat-feedback/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Feedback not found."
