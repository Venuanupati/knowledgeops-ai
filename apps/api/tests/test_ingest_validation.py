import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_ingest_unsupported_file_type():
    response = client.post(
        "/api/v1/ingest",
        files={
            "file": (
                "sample.csv",
                b"name,value\nsample,123",
                "text/csv",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == ("Unsupported file type: .csv. Allowed types are: .pdf, .txt, .docx")
