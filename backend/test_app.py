import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


def _load_env() -> Path | None:
    base_dir = Path(__file__).parent.resolve()
    for env_path in (base_dir.parent / ".env", Path.cwd() / ".env", base_dir / ".env"):
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return env_path
    return None


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def _normalize_email_config() -> dict:
    smtp_host = _get_env("SMTP_HOST", "")
    smtp_port = int(_get_env("SMTP_PORT", "587"))
    smtp_user = _get_env("SMTP_USER", "").strip()
    smtp_pass = "".join(_get_env("SMTP_PASS", "").split())  # remove spaces/newlines
    recipient_email = _get_env("RECIPIENT_EMAIL", smtp_user)
    sender_email = _get_env("SENDER_EMAIL", smtp_user)
    disable_email = _get_env("DISABLE_EMAIL", "1").strip().lower()
    smtp_ssl = _get_env("SMTP_SSL", "").strip().lower()

    return {
        "smtp_host": smtp_host,
        "smtp_port": smtp_port,
        "smtp_user": smtp_user,
        "smtp_pass": smtp_pass,
        "recipient_email": recipient_email,
        "sender_email": sender_email,
        "disable_email": disable_email,
        "smtp_ssl": smtp_ssl,
    }


def _auth_details(err: smtplib.SMTPAuthenticationError) -> str:
    try:
        raw = err.smtp_error
        if isinstance(raw, bytes):
            raw_text = raw.decode("utf-8", errors="replace")
        else:
            raw_text = str(raw)
    except Exception:
        raw_text = ""
    code = getattr(err, "smtp_code", None)
    if code is None:
        return raw_text.strip() or "authentication failed"
    return f"{code} {raw_text.strip()}".strip()


def send_test_email() -> None:
    loaded_env = _load_env()
    cfg = _normalize_email_config()

    print("Loaded .env:", str(loaded_env) if loaded_env else "<none>")
    print(
        "Effective config:",
        {
            "DISABLE_EMAIL": cfg["disable_email"],
            "SMTP_HOST": cfg["smtp_host"],
            "SMTP_PORT": cfg["smtp_port"],
            "SMTP_SSL": cfg["smtp_ssl"],
            "SMTP_USER": cfg["smtp_user"],
            "RECIPIENT_EMAIL": cfg["recipient_email"],
        },
    )

    if cfg["disable_email"] in ("1", "true", "yes"):
        raise RuntimeError("Email sending is disabled (DISABLE_EMAIL=1). Set DISABLE_EMAIL=0 in .env")

    missing = [
        name
        for name, val in (
            ("SMTP_HOST", cfg["smtp_host"]),
            ("SMTP_USER", cfg["smtp_user"]),
            ("SMTP_PASS", cfg["smtp_pass"]),
            ("RECIPIENT_EMAIL", cfg["recipient_email"]),
        )
        if not val
    ]
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

    subject = "Sharpmind Labs — SMTP Test Email"
    body = (
        "This is a test email from backend/test_app.py.\n\n"
        "If you received this, SMTP is working.\n"
    )

    msg = EmailMessage()
    msg["From"] = cfg["sender_email"]
    msg["To"] = cfg["recipient_email"]
    msg["Subject"] = subject
    msg.set_content(body)

    primary_use_ssl = cfg["smtp_ssl"] in ("1", "true", "yes") or cfg["smtp_port"] == 465
    attempts = [
        {"use_ssl": primary_use_ssl, "port": cfg["smtp_port"], "label": "configured"},
    ]
    if cfg["smtp_host"].lower().strip() == "smtp.gmail.com" and not primary_use_ssl and cfg["smtp_port"] == 587:
        attempts.append({"use_ssl": True, "port": 465, "label": "gmail_fallback_ssl_465"})

    errors: list[str] = []
    for attempt in attempts:
        use_ssl = bool(attempt["use_ssl"])
        port = int(attempt["port"])
        label = str(attempt["label"])
        smtp_cls = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP

        try:
            with smtp_cls(cfg["smtp_host"], port, timeout=20) as server:
                server.ehlo()
                if not use_ssl:
                    server.starttls()
                    server.ehlo()
                server.login(cfg["smtp_user"], cfg["smtp_pass"])
                server.send_message(msg)
                print(f"OK: sent test email via {label} (port {port}) to {cfg['recipient_email']}")
                return
        except smtplib.SMTPAuthenticationError as auth_err:
            errors.append(f"{label}: {_auth_details(auth_err)}")
        except Exception as err:
            errors.append(f"{label}: {type(err).__name__}: {err}")

    raise RuntimeError("SMTP send failed. Details: " + "; ".join(errors))


if __name__ == "__main__":
    send_test_email()
