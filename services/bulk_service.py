from models import Job
from services.certificate_service import generate_one_certificate


def process_job(db, job: Job, event_name: str):
    certificates = job.certificates

    for certificate in certificates:
        try:
            path = generate_one_certificate(
                certificate,
                event_name
            )

            certificate.status = "success"
            certificate.file_path = path
            job.success_count += 1

        except Exception as error:
            certificate.status = "failed"
            certificate.error_message = str(error)
            job.failure_count += 1

    job.status = "completed"

    db.commit()