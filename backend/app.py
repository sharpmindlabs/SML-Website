import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env (best-effort).
# We try a few sensible locations to support both local runs and containers.
BASE_DIR = Path(__file__).parent.resolve()
ENV_CANDIDATES = [
    BASE_DIR.parent / ".env",
    Path.cwd() / ".env",
    BASE_DIR / ".env",
]
for env_path in ENV_CANDIDATES:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
        break

# Serve static files from frontend directory (best-effort; nginx serves frontend in Docker).
FRONTEND_DIR_CANDIDATES = [
    BASE_DIR.parent / "frontend",  # repo layout: <root>/backend/app.py
    Path("/app/frontend"),         # docker-compose volume mount
]

static_dir = None
for candidate in FRONTEND_DIR_CANDIDATES:
    if candidate.exists():
        static_dir = str(candidate.resolve())
        break
if static_dir is None:
    static_dir = str((BASE_DIR.parent / "frontend").resolve())

app = Flask(__name__, static_folder=static_dir, static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Company address (as requested)
COMPANY_ADDRESS = "19, Thiruvalluvar Street, Sathyamangalam, Erode"

# Email configuration from environment
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "nakulvelusamyperumalgounder@gmail.com")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USER)
DISABLE_EMAIL = os.getenv("DISABLE_EMAIL", "").lower()


def send_email(subject: str, body: str) -> None:
    # Dev mode: allow local testing without SMTP
    if DISABLE_EMAIL in ("1", "true", "yes"):  # no-op in dev
        return
    missing = [
        name for name, val in (
            ("SMTP_HOST", SMTP_HOST),
            ("SMTP_USER", SMTP_USER),
            ("SMTP_PASS", SMTP_PASS),
            ("RECIPIENT_EMAIL", RECIPIENT_EMAIL),
        ) if not val
    ]
    if missing:
        raise RuntimeError(
            f"SMTP configuration missing: {', '.join(missing)}. Set these in environment variables or .env"
        )

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        # Be explicit with EHLO to avoid TLS/auth quirks
        server.ehlo()
        server.starttls()
        server.ehlo()
        try:
            server.login(SMTP_USER, SMTP_PASS)
        except smtplib.SMTPAuthenticationError as auth_err:
            raise RuntimeError(
                "SMTP authentication failed. For Gmail, ensure 2-Step Verification is enabled and use a 16-character App Password for SMTP. Verify that SMTP_USER matches the same Gmail account and that the app password is correct."
            ) from auth_err
        server.send_message(msg)


@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return app.send_static_file(filename)
    except:
        return app.send_static_file('index.html')

@app.post("/api/contact")
def api_contact():
    data = request.form or request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    organization = data.get("organization", "").strip()
    inquiry_type = data.get("inquiry_type", "").strip()
    message = data.get("message", "").strip()

    # Frontend default placeholder; treat it as not-provided.
    if inquiry_type.lower() in ("select topic", "select", "-", "none"):
        inquiry_type = ""

    # Basic validation
    missing = [
        field for field, value in (
            ("full_name", full_name),
            ("email", email),
            ("message", message),
        ) if not value
    ]
    if missing:
        return jsonify({"ok": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

    subject = f"Sharpmind Labs — New Contact: {full_name}"
    body_lines = [
        "A new contact form submission was received:",
        "",
        f"Name: {full_name}",
        f"Email: {email}",
        f"Organization: {organization or '-'}",
        f"Inquiry Type: {inquiry_type or '-'}",
        "",
        "Message:",
        message,
        "",
        f"Company Address: {COMPANY_ADDRESS}",
    ]
    body = "\n".join(body_lines)

    try:
        send_email(subject, body)
        return jsonify({"ok": True, "message": "Submission sent successfully."})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'service': 'SML Website'}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)