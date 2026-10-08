from fastapi import FastAPI
from schemas import CertificateJobRequest
from database import SessionLocal
from models import Job, Certificate

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

        return {
            "job_id": job.id,
            "status": job.status,
            "total_count": job.total_count
        }


    finally:db.close()
