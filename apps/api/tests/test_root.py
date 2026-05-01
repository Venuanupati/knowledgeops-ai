import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["app"] == "knowledgeops-ai"
    assert data["environment"] == "local"
    assert data["message"] == "KnowledgeOps AI API is running."
    assert data["docs_url"] == "/docs"
    assert data["health_url"] == "/api/v1/health"
