import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_chat_empty_question():
    response = client.post("/api/v1/chat", json={"question": ""})

    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty."


def test_chat_too_short_question():
    response = client.post("/api/v1/chat", json={"question": "Hi"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Question is too short. Minimum length is 3 characters."


def test_chat_invalid_top_k_too_high():
    response = client.post("/api/v1/chat", json={"question": "What is the leave policy?", "top_k": 50})

    assert response.status_code == 400
    assert response.json()["detail"] == "top_k must be between 1 and 10."


def test_chat_invalid_top_k_too_low():
    response = client.post("/api/v1/chat", json={"question": "What is the leave policy?", "top_k": 0})

    assert response.status_code == 400
    assert response.json()["detail"] == "top_k must be between 1 and 10."
