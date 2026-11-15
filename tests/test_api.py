
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running"


def test_valid_posting_request(monkeypatch):

    async def fake_publish_message(message):
        return {
            "success": True,
            "results": [
                {
                    "platform": "Mastodon",
                    "status": "success",
                    "posted_url": "https://example.com/post/1",
                    "public_access": True,
                    "date": "2026-11-15",
                    "time": "12:00:00",
                    "error": None
                }
            ]
        }

    monkeypatch.setattr(
        "app.main.publish_message",
        fake_publish_message
    )

    response = client.post(
        "/postingRequest",
        json={
            "message": "Check this out: https://example.com"
        }
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["results"][0]["platform"] == "Mastodon"


def test_invalid_posting_request():

    response = client.post(
        "/postingRequest",
        json={
            "message": "Hello everyone!"
        }
    )

    assert response.status_code == 422
