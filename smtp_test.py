import os
from dotenv import load_dotenv

# Load env from project root
load_dotenv()

from app import send_email

if __name__ == "__main__":
    subject = "SMTP Test"
    body = "This is a test email from smtp_test.py"
    try:
        send_email(subject, body)
        print("OK: Email sent successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
