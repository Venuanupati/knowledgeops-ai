import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.integration

client = TestClient(app)


def test_chat_logs_list_response_shape():
    response = client.get("/api/v1/chat-logs")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data

    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)
    assert isinstance(data["limit"], int)
    assert isinstance(data["offset"], int)


def test_chat_summary_response_shape():
    response = client.get("/api/v1/chat-summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_chats" in data
    assert "high_confidence_count" in data
    assert "medium_confidence_count" in data
    assert "low_confidence_count" in data

    assert isinstance(data["total_chats"], int)
    assert isinstance(data["high_confidence_count"], int)
    assert isinstance(data["medium_confidence_count"], int)
    assert isinstance(data["low_confidence_count"], int)


def test_chat_feedback_list_response_shape():
    response = client.get("/api/v1/chat-feedback")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data

    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)
    assert isinstance(data["limit"], int)
    assert isinstance(data["offset"], int)


def test_chat_feedback_summary_response_shape():
    response = client.get("/api/v1/chat-feedback-summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_feedback" in data
    assert "up_count" in data
    assert "down_count" in data

    assert isinstance(data["total_feedback"], int)
    assert isinstance(data["up_count"], int)
    assert isinstance(data["down_count"], int)
