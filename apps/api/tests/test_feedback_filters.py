import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_chat_feedback_invalid_rating_filter():
    response = client.get("/api/v1/chat-feedback?rating=maybe")

    assert response.status_code == 400
    assert response.json()["detail"] == "rating must be one of: up, down."
