import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_chat_success_mocked(monkeypatch):
    def mock_answer_question(question, document_id=None, top_k=None):
        return (
            "Employees get 15 paid leave days annually [SOURCE 1].",
            [
                {
                    "document_id": 1,
                    "chunk_id": 10,
                    "filename": "employee_handbook.pdf",
                    "chunk_index": 2,
                    "score": 0.91,
                    "text": "Employees get 15 paid leave days annually.",
                }
            ],
            "high",
        )

    monkeypatch.setattr(
        "app.api.routes.chat.answer_question",
        mock_answer_question,
    )

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is the leave policy?",
            "include_sources": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Employees get 15 paid leave days annually [SOURCE 1]."
    assert data["confidence"] == "high"
    assert len(data["sources"]) == 1

    source = data["sources"][0]
    assert source["document_id"] == 1
    assert source["chunk_id"] == 10
    assert source["filename"] == "employee_handbook.pdf"
    assert source["chunk_index"] == 2
    assert source["score"] == 0.91
    assert source["snippet"] == "Employees get 15 paid leave days annually."


def test_chat_success_mocked_without_sources(monkeypatch):
    def mock_answer_question(question, document_id=None, top_k=None):
        return (
            "Employees get 15 paid leave days annually [SOURCE 1].",
            [
                {
                    "document_id": 1,
                    "chunk_id": 10,
                    "filename": "employee_handbook.pdf",
                    "chunk_index": 2,
                    "score": 0.91,
                    "text": "Employees get 15 paid leave days annually.",
                }
            ],
            "high",
        )

    monkeypatch.setattr(
        "app.api.routes.chat.answer_question",
        mock_answer_question,
    )

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is the leave policy?",
            "include_sources": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Employees get 15 paid leave days annually [SOURCE 1]."
    assert data["confidence"] == "high"
    assert data["sources"] == []


def test_chat_low_confidence_mocked(monkeypatch):
    def mock_answer_question(question, document_id=None, top_k=None):
        return (
            "I could not confidently answer that from the provided documents. "
            "Try asking a more specific question or select the correct document.",
            [
                {
                    "document_id": 1,
                    "chunk_id": 11,
                    "filename": "employee_handbook.pdf",
                    "chunk_index": 4,
                    "score": 0.42,
                    "text": "This chunk is weakly related to the question.",
                }
            ],
            "low",
        )

    monkeypatch.setattr(
        "app.api.routes.chat.answer_question",
        mock_answer_question,
    )

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is the space travel reimbursement policy?",
            "include_sources": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "I could not confidently answer that from the provided documents. "
        "Try asking a more specific question or select the correct document."
    )
    assert data["confidence"] == "low"
    assert len(data["sources"]) == 1
    assert data["sources"][0]["score"] == 0.42


def test_chat_passes_document_id_and_top_k(monkeypatch):
    captured_args = {}

    def mock_answer_question(question, document_id=None, top_k=None):
        captured_args["question"] = question
        captured_args["document_id"] = document_id
        captured_args["top_k"] = top_k

        return (
            "Mocked answer [SOURCE 1].",
            [
                {
                    "document_id": document_id,
                    "chunk_id": 20,
                    "filename": "selected_document.pdf",
                    "chunk_index": 1,
                    "score": 0.88,
                    "text": "Selected document content.",
                }
            ],
            "high",
        )

    monkeypatch.setattr(
        "app.api.routes.chat.answer_question",
        mock_answer_question,
    )

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What does this selected document say?",
            "document_id": 7,
            "top_k": 3,
            "include_sources": True,
        },
    )

    assert response.status_code == 200

    assert captured_args["question"] == "What does this selected document say?"
    assert captured_args["document_id"] == 7
    assert captured_args["top_k"] == 3

    data = response.json()

    assert data["answer"] == "Mocked answer [SOURCE 1]."
    assert data["confidence"] == "high"
    assert data["sources"][0]["document_id"] == 7
