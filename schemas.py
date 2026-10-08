from pydantic import BaseModel, EmailStr, Field


class Recipient(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr


class CertificateJobRequest(BaseModel):
    event_name: str = Field(min_length=1)
    recipients: list[Recipient] = Field(min_length=1)