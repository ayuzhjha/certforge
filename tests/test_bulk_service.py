from unittest.mock import patch

from services.bulk_service import process_job


def test_one_certificate_failure_does_not_stop_job():

    class FakeCertificate:
        def __init__(self, name):
            self.recipient_name = name
            self.recipient_email = f"{name.lower()}@example.com"
            self.status = "pending"
            self.file_path = None
            self.error_message = None

    class FakeJob:
        def __init__(self):
            self.certificates = [
                FakeCertificate("Alice"),
                FakeCertificate("Bob"),
                FakeCertificate("Charlie"),
            ]
            self.success_count = 0
            self.failure_count = 0
            self.status = "processing"

    class FakeDB:
        def commit(self):
            pass

    job = FakeJob()
    db = FakeDB()

    def fake_generator(certificate, event_name):
        if certificate.recipient_name == "Bob":
            raise Exception("Simulated generation failure")

        return f"certificates/{certificate.recipient_name}.pdf"

    with patch(
        "services.bulk_service.generate_one_certificate",
        side_effect=fake_generator
    ):
        process_job(db, job, "Test Event")

    assert job.success_count == 2
    assert job.failure_count == 1
    assert job.status == "completed"

    assert job.certificates[0].status == "success"
    assert job.certificates[1].status == "failed"
    assert job.certificates[2].status == "success"