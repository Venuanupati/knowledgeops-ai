import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_delete_document_not_found():
    response = client.delete("/api/v1/documents/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def test_reindex_document_not_found():
    response = client.post("/api/v1/documents/999999/reindex")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."
