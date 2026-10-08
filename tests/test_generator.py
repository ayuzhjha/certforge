from pydantic import ValidationError
import pytest

from schemas import CertificateJobRequest


def test_empty_recipients_rejected():
    with pytest.raises(ValidationError):
        CertificateJobRequest(
            event_name="Test Event",
            recipients=[]
        )


def test_invalid_email_rejected():
    with pytest.raises(ValidationError):
        CertificateJobRequest(
            event_name="Test Event",
            recipients=[
                {
                    "name": "Alice",
                    "email": "not-an-email"
                }
            ]
        )


def test_valid_request_accepted():
    request = CertificateJobRequest(
        event_name="Test Event",
        recipients=[
            {
                "name": "Alice",
                "email": "alice@example.com"
            }
        ]
    )

    assert request.event_name == "Test Event"
    assert len(request.recipients) == 1