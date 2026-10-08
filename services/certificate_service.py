import os

from generator import generate_certificate


def generate_one_certificate(certificate, event_name):
    os.makedirs("certificates", exist_ok=True)

    filename = f"{certificate.id}_{certificate.recipient_name}.pdf"
    output_path = os.path.join("certificates", filename)

    generate_certificate(
        name=certificate.recipient_name,
        event_name=event_name,
        output_path=output_path
    )

    return output_path