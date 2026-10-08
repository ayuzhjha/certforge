from fastapi import FastAPI
from schemas import CertificateJobRequest
from database import SessionLocal
from models import Job, Certificate
from services.bulk_service import process_job
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Bulk Certificate Generator API"}

@app.post("/jobs")
def create_job(request: CertificateJobRequest):
    db = SessionLocal()

    try:
        job = Job(
            status="pending",
            total_count=len(request.recipients)
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        for recipient in request.recipients:
            certificate = Certificate(
                job_id=job.id,
                recipient_name=recipient.name,
                recipient_email=recipient.email,
                status="pending"
            )

            db.add(certificate)

        db.commit()

        process_job(
            db=db,
            job=job,
            event_name=request.event_name
        )

        return {
            "job_id": job.id,
            "status": job.status,
           "total_count": job.total_count,
            "success_count": job.success_count,
            "failure_count": job.failure_count
        }


    finally:db.close()
    
@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return {"error": "Job not found"}

        return {
            "job_id": job.id,
            "status": job.status,
            "total_count": job.total_count,
            "success_count": job.success_count,
            "failure_count": job.failure_count
        }

    finally:
        db.close()

@app.get("/certificates/{certificate_id}")
def get_certificate(certificate_id: int):
    db = SessionLocal()

    try:
        certificate = (
            db.query(Certificate)
            .filter(Certificate.id == certificate_id)
            .first()
        )

        if not certificate:
            return {"error": "Certificate not found"}

        if certificate.status != "success":
            return {"error": "Certificate is not available"}

        return FileResponse(
            path=certificate.file_path,
            media_type="application/pdf",
            filename=f"{certificate.recipient_name}.pdf"
        )

    finally:
        db.close()