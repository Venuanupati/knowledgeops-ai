import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.integration

client = TestClient(app)


def test_status():
    response = client.get("/api/v1/status")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "total_documents" in data
    assert "total_chats" in data
    assert "total_feedback" in data

    assert isinstance(data["total_documents"], int)
    assert isinstance(data["total_chats"], int)
    assert isinstance(data["total_feedback"], int)
