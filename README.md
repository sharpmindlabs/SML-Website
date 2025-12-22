# SML-Website

Sharp Mind Labs official website with Flask backend and responsive frontend.

## Project Structure
```
your-repo/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── productoverview.html
│   ├── solution.html
│   └── assets/
├── docker-compose.yml
├── nginx.conf
└── .github/
    └── workflows/
        └── deploy.yml
```

## Quick Start
```bash
# Run with Docker Compose
docker-compose up -d

# Or run backend only
cd backend
pip install -r requirements.txt
python app.py
```

## URLs
- Home: http://localhost/
- About: http://localhost/about.html
- Products: http://localhost/productoverview.html
- Solutions: http://localhost/solution.html
- Contact: http://localhost/contact.html
- API Health: http://localhost/api/health

## CI/CD Pipeline
Automated deployment via GitHub Actions on push to main branch.