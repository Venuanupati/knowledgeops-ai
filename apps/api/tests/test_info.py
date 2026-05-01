import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_info():
    response = client.get("/api/v1/info")

    assert response.status_code == 200

    data = response.json()

    assert data["app"] == "knowledgeops-ai"
    assert data["environment"] == "local"
    assert data["api_version"] == "v1"
    assert data["docs_url"] == "/docs"
    assert data["health_url"] == "/api/v1/health"
