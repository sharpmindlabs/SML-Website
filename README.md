# SML-Website

Sharpmind Labs official website - AI Software Product Company

## About

Sharpmind Labs develops cutting-edge AI software products that transform businesses. From intelligent automation to machine learning solutions, we build AI-powered applications that deliver measurable results and competitive advantages.

## Project Structure
```
SML-Website/
├── backend/
│   ├── app.py              # Flask backend
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/
│   └── index.html         # Main website
├── docker-compose.yml     # Multi-container setup
├── nginx.conf            # Reverse proxy config
└── .github/
    └── workflows/
        └── deploy.yml    # CI/CD pipeline
```

## Quick Start

### Local Development
```bash
# Run backend only
cd backend
pip install -r requirements.txt
python app.py
```

### Docker Deployment
```bash
# Run full stack with Docker Compose
docker compose up -d

# Check health
curl http://localhost/healthz
```

### HTTPS with Let's Encrypt (Docker Nginx)

If you run Nginx inside Docker (this repo does), the host port `80` is already in use by the container. The Certbot `--nginx` installer tries to restart the *system* nginx on the host and will fail with bind-to-80 errors.

Recommended approach:
1) Stop Docker briefly, obtain/renew cert using standalone mode:
```bash
cd ~/SML-Website
docker compose down

# Obtain or renew
sudo certbot certonly --standalone -d dev.sharpmindlabs.com
```

2) Start the stack with SSL enabled (expects certs at `/etc/letsencrypt` on the host):
```bash
docker compose -f docker-compose.yml -f docker-compose.ssl.yml up -d --build
```

When running with the SSL overlay, the site is HTTPS-only (`:443`). Port `80` is not exposed.

If you already have a cert but installation failed, just run:
```bash
sudo certbot renew --standalone
```

## URLs
- Home: http://localhost/
- API Health: http://localhost/api/health
- Contact API: http://localhost/api/contact

## CI/CD Pipeline
Automated deployment via GitHub Actions on push to main branch.

## Tech Stack
- **Backend**: Python Flask, Gunicorn
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Infrastructure**: Docker, Nginx
- **CI/CD**: GitHub Actions

## Environment Variables
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SSL=0
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-gmail-app-password
RECIPIENT_EMAIL=contact@sharpmindlabs.com
DISABLE_EMAIL=1  # Set to 0 to enable sending
```

Notes (Gmail):
- Use a Gmail "App Password" (requires 2-Step Verification). Your normal Gmail password usually will not work for SMTP.
- Keep `SMTP_USER` and the App Password from the same Gmail account.

Docker / CI note:
- `docker-compose.yml` treats `.env` as optional (so CI/CD won't fail if it's not present).
- To enable real email sending in production, provide `SMTP_*` and set `DISABLE_EMAIL=0` via a `.env` on the server or via your deployment secrets.

## Deployment
Push to main branch triggers automatic deployment:
1. Tests run
2. Docker images build
3. Health checks verify
4. Production deployment

---
© 2025 Sharpmind Labs. All rights reserved.