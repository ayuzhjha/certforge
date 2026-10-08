from fastapi.testclient import TestClient
from database import SessionLocal
from models import Certificate

from main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Test Event",
            "recipients": [
                {
                    "name": "Alice",
                    "email": "alice@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total_count"] == 1
    assert data["status"] == "pending"


def test_get_job_status():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Status Test",
            "recipients": [
                {
                    "name": "Alice",
                    "email": "alice@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    status_response = client.get(f"/jobs/{job_id}")

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["job_id"] == job_id
    assert data["total_count"] == 1
    
def test_get_nonexistent_job():
    response = client.get("/jobs/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
    
def test_get_certificate():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Certificate Test",
            "recipients": [
                {
                    "name": "Alice",
                    "email": "alice@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    db = SessionLocal()

    try:
        certificate = (
            db.query(Certificate)
            .filter(Certificate.job_id == job_id)
            .first()
        )

        assert certificate is not None
        assert certificate.status == "success"

        certificate_response = client.get(
            f"/certificates/{certificate.id}"
        )

        assert certificate_response.status_code == 200
        assert certificate_response.headers["content-type"] == "application/pdf"

    finally:
        db.close()
        
def test_get_nonexistent_certificate():
    response = client.get("/certificates/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Certificate not found"