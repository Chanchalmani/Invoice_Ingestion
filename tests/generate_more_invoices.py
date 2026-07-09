import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_invoice_pdf(filename, inv_num, date, due, vendor, uid, iban, items, net, vat, gross, currency, cost_center):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"INVOICE # {inv_num}")
    
    # Invoice Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {date}")
    c.drawString(50, height - 100, f"Due: {due}")
    
    # Vendor Details
    c.drawString(50, height - 130, f"Vendor: {vendor}")
    c.drawString(50, height - 150, f"Vendor UID: {uid}")
    c.drawString(50, height - 170, f"IBAN: {iban}")
    
    # Line Items Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 210, "Line Items:")
    
    # Line Items
    c.setFont("Helvetica", 12)
    y_pos = height - 230
    for item in items:
        c.drawString(70, y_pos, item)
        y_pos -= 20
        
    y_pos -= 20 # Add space before totals
    
    # Totals
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, f"Net: {net}")
    c.drawString(50, y_pos - 20, f"VAT 20%: {vat}")
    c.drawString(50, y_pos - 40, f"Gross: {gross}")
    
    # Other Details
    c.setFont("Helvetica", 12)
    c.drawString(50, y_pos - 70, f"Currency: {currency}")
    c.drawString(50, y_pos - 90, f"Cost Center: {cost_center}")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Thank you for your business!")
    
    c.save()
    print(f"Created sample invoice at {filename}")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    
    # Invoice 2: Marketing Services
    output_path_2 = os.path.join(base_dir, "sample_invoice_2.pdf")
    create_invoice_pdf(
        filename=output_path_2,
        inv_num="MKT-9942",
        date="2026-07-02",
        due="2026-07-16",
        vendor="Global Media Partners",
        uid="GMP998877",
        iban="GB8220012311122333",
        items=[
            "- Social Media Campaign @ 1500.00 = 1500.00",
            "- Graphic Design Retainer @ 500.00 = 500.00"
        ],
        net="2000.00",
        vat="400.00",
        gross="2400.00",
        currency="GBP",
        cost_center="Marketing"
    )

    # Invoice 3: Cloud Infrastructure
    output_path_3 = os.path.join(base_dir, "sample_invoice_3.pdf")
    create_invoice_pdf(
        filename=output_path_3,
        inv_num="AWS-0099112",
        date="2026-07-03",
        due="2026-07-10",
        vendor="Cloud Compute Inc",
        uid="CCI-554433",
        iban="US998877665544332211",
        items=[
            "- Compute Instances (July) @ 3000.00 = 3000.00",
            "- S3 Storage @ 250.00 = 250.00",
            "- Database Hosting @ 750.00 = 750.00"
        ],
        net="4000.00",
        vat="800.00",
        gross="4800.00",
        currency="USD",
        cost_center="Engineering"
    )
