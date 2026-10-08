from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def generate_certificate(name: str, event_name: str, output_path: str):
    if name == "FAIL":
        raise Exception("Intentional test failure")
    
    pdf = canvas.Canvas(output_path, pagesize=A4)

    width, height = A4

    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 150,
        "Certificate of Participation"
    )

    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(
        width / 2,
        height - 220,
        "This certificate is proudly presented to"
    )

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 280,
        name
    )

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 340,
        f"for participating in {event_name}"
    )

    pdf.save()