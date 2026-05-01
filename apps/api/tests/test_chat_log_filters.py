import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_chat_logs_invalid_confidence_filter():
    response = client.get("/api/v1/chat-logs?confidence=unknown")

    assert response.status_code == 400
    assert response.json()["detail"] == "confidence must be one of: high, medium, low."
