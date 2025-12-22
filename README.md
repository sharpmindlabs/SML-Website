# SML-Website

Shapmind Labs official website - AI Software Product Company

## About

Shapmind Labs develops cutting-edge AI software products that transform businesses. From intelligent automation to machine learning solutions, we build AI-powered applications that deliver measurable results and competitive advantages.

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
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-password
RECIPIENT_EMAIL=contact@sharpmindlabs.com
DISABLE_EMAIL=1  # For local development
```

## Deployment
Push to main branch triggers automatic deployment:
1. Tests run
2. Docker images build
3. Health checks verify
4. Production deployment

---
© 2025 Shapmind Labs. All rights reserved.