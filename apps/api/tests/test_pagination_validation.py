import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_documents_invalid_limit():
    response = client.get("/api/v1/documents?limit=0")

    assert response.status_code == 400
    assert response.json()["detail"] == "limit must be between 1 and 100."


def test_documents_invalid_offset():
    response = client.get("/api/v1/documents?offset=-1")

    assert response.status_code == 400
    assert response.json()["detail"] == "offset must be 0 or greater."
