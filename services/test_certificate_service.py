from database import SessionLocal
from models import Certificate
from services.certificate_service import generate_one_certificate


db = SessionLocal()

try:
    certificate = db.query(Certificate).first()

    path = generate_one_certificate(
        certificate=certificate,
        event_name="Hackathon"
    )

    certificate.status = "success"
    certificate.file_path = path

    db.commit()

    print("Certificate generated:", path)

finally:
    db.close()