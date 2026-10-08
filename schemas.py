from pydantic import BaseModel, EmailStr

class Recipient(BaseModel):
    name: str
    email: EmailStr

class CertificateJobRequest(BaseModel):
    event_name: str
    recipients: list[Recipient]

    