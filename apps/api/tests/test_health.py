import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.integration

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "postgres" in data
    assert "qdrant" in data

    assert data["status"] in {"ok", "degraded"}
    assert data["postgres"] in {"ok", "down"}
    assert data["qdrant"] in {"ok", "down"}
