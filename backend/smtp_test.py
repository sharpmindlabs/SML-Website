import os
from dotenv import load_dotenv
from pathlib import Path

# Load root .env explicitly
ROOT_ENV = Path(__file__).resolve().parents[1] / ".env"
if ROOT_ENV.exists():
    load_dotenv(dotenv_path=ROOT_ENV)

from app import send_email  # import from backend.app

if __name__ == "__main__":
    subject = "Backend SMTP Test"
    body = "This is a test email from backend/smtp_test.py"
    try:
        send_email(subject, body)
        print("OK: Backend email sent successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
