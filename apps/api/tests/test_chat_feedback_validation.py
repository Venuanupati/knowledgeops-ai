import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_chat_feedback_invalid_rating():
    response = client.post(
        "/api/v1/chat-feedback",
        json={
            "chat_id": 1,
            "rating": "maybe",
            "comment": "Invalid rating test",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Rating must be 'up' or 'down'."


def test_chat_feedback_chat_not_found():
    response = client.post(
        "/api/v1/chat-feedback",
        json={
            "chat_id": 999999,
            "rating": "up",
            "comment": "Chat does not exist",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat log not found."
