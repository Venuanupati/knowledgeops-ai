import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_documents_invalid_status_filter():
    response = client.get("/api/v1/documents?status=failed")

    assert response.status_code == 400
    assert response.json()["detail"] == "status must be one of: uploaded, chunked, indexed."
