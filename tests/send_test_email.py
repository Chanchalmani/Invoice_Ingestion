import smtplib
from email.message import EmailMessage
import os

# Load credentials from .env file securely
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

# --- SMTP DETAILS ---
SMTP_SERVER = "smtp.ethereal.email"
SMTP_PORT = 587
USERNAME = os.environ.get("ETHEREAL_EMAIL")
PASSWORD = os.environ.get("ETHEREAL_PASSWORD")
# ---------------------------------------------

def send_invoice_email():
    msg = EmailMessage()
    msg['Subject'] = 'New Invoice Attached'
    msg['From'] = USERNAME
    msg['To'] = USERNAME
    msg.set_content('Please find the attached invoice for processing.')

    # Attach the PDF
    pdf_path = os.path.join(os.path.dirname(__file__), "sample_invoice_3.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"Error: Could not find {pdf_path}. Did you run generate_sample_invoice.py first?")
        return

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='sample_invoice.pdf')

    try:
        print("Connecting to SMTP server...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)
            print("Successfully sent the test email with the PDF attached!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_invoice_email()
