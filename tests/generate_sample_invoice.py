import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_invoice_pdf(filename="sample_invoice.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "INVOICE # INV-2026-001")
    
    # Invoice Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Date: 2026-07-01")
    c.drawString(50, height - 100, "Due: 2026-07-31")
    
    # Vendor Details
    c.drawString(50, height - 130, "Vendor: Acme Supplies")
    c.drawString(50, height - 150, "Vendor UID: ACME123")
    c.drawString(50, height - 170, "IBAN: DE89370400440532013000")
    
    # Line Items Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 210, "Line Items:")
    
    # Line Items
    c.setFont("Helvetica", 12)
    c.drawString(70, height - 230, "- 10 x Laptops @ 80.00 = 800.00")
    c.drawString(70, height - 250, "- 5 x Monitors @ 40.00 = 200.00")
    
    # Totals
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 290, "Net: 1000.00")
    c.drawString(50, height - 310, "VAT 20%: 200.00")
    c.drawString(50, height - 330, "Gross: 1200.00")
    
    # Other Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 360, "Currency: EUR")
    c.drawString(50, height - 380, "Cost Center: IT")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Thank you for your business!")
    
    c.save()
    print(f"Created sample invoice at {filename}")

if __name__ == "__main__":
    # Ensure tests directory exists or create file in current directory
    output_path = os.path.join(os.path.dirname(__file__), "sample_invoice.pdf")
    create_invoice_pdf(output_path)
