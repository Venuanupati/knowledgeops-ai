from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_chat_feedback_success_mocked(monkeypatch):
    mock_chat_log = SimpleNamespace(id=1)

    mock_feedback = SimpleNamespace(
        id=10,
        chat_id=1,
        rating="up",
        comment="Helpful answer.",
    )

    def mock_get_chat_log_by_id(db, chat_id):
        assert chat_id == 1
        return mock_chat_log

    def mock_create_chat_feedback(db, chat_id, rating, comment=None):
        assert chat_id == 1
        assert rating == "up"
        assert comment == "Helpful answer."
        return mock_feedback

    monkeypatch.setattr(
        "app.api.routes.chat_feedback.get_chat_log_by_id",
        mock_get_chat_log_by_id,
    )

    monkeypatch.setattr(
        "app.api.routes.chat_feedback.create_chat_feedback",
        mock_create_chat_feedback,
    )

    response = client.post(
        "/api/v1/chat-feedback",
        json={
            "chat_id": 1,
            "rating": "up",
            "comment": "Helpful answer.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["feedback_id"] == 10
    assert data["chat_id"] == 1
    assert data["rating"] == "up"
    assert data["comment"] == "Helpful answer."
    assert data["message"] == "Feedback submitted successfully."
