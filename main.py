from fastapi import FastAPI
from schemas import CertificateJobRequest

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Bulk Certificate Generator API"}

@app.post("/jobs")
def create_job(request: CertificateJobRequest):
    return {
        "message": "Job Recieved",
        "event_name": "request.event_name",
        "reciepient_count": "len(request.recipients)"
    }