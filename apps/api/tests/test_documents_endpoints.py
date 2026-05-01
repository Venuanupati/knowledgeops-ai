import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.integration

client = TestClient(app)


def test_documents_list_response_shape():
    response = client.get("/api/v1/documents")

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


def test_documents_summary_response_shape():
    response = client.get("/api/v1/documents-summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_documents" in data
    assert "uploaded_count" in data
    assert "chunked_count" in data
    assert "indexed_count" in data

    assert isinstance(data["total_documents"], int)
    assert isinstance(data["uploaded_count"], int)
    assert isinstance(data["chunked_count"], int)
    assert isinstance(data["indexed_count"], int)
