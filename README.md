# TrusthLens

> Spot misinformation. Understand why. Share confidence.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-6366f1?style=for-the-badge)](https://trusthlens.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Model-f7931e?style=for-the-badge)](https://scikit-learn.org/)

TrusthLens is an explainable, AI-powered news classifier that gives a fast verdict — REAL NEWS or FAKE NEWS — plus a confidence score and keyword-level explanations. It combines a lightweight TF‑IDF + PassiveAggressiveClassifier pipeline with a user-facing Flask dashboard for saving history and generating shareable PDF reports.

---

## Table of Contents

- [Highlights](#highlights)
- [Quick Demo](#quick-demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How it works](#how-it-works)
- [Getting started (local)](#getting-started-local)
- [Build the model](#build-the-model)
- [Run the app](#run-the-app)
- [Prediction API](#prediction-api)
- [Database & persistence](#database--persistence)
- [Deployment notes](#deployment-notes)
- [Development & testing](#development--testing)
- [Contributing](#contributing)
- [Security & privacy](#security--privacy)
- [Future ideas](#future-ideas)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Highlights

- Instant article verdicts with a numeric confidence score.
- Explainable AI: top TF‑IDF words that influenced the prediction.
- User accounts, history, and personal dashboard.
- PDF report generation for sharing results.
- Responsive UI (HTML/CSS/JS + Bootstrap).
- Deployment‑ready (Gunicorn + Procfile).

---

## Quick Demo

Open the hosted demo:
https://trusthlens.onrender.com

---

## Tech Stack

- Languages: Python (backend), HTML/CSS/JavaScript (frontend)
- Framework: Flask
- ML: scikit-learn (TfidfVectorizer + PassiveAggressiveClassifier)
- Persistence: SQLite (lightweight instance DB)
- PDF reports: reportlab
- Deployment: Gunicorn, compatible with Render, Heroku-style Procfile

Notable packages (see requirements.txt): Flask, scikit-learn, pandas, reportlab, gunicorn

---

## Project Structure

```
TrusthLens/
├── app.py                      # Flask application + routes
├── bootstrap_model.py          # Train/save model & vectorizer (creates models/)
├── predict.py                  # Model loading, prediction & explanation
├── model_metrics.py            # Load saved metrics (models/metrics.json)
├── services/
│   └── report_generator.py     # Generate PDF reports
├── database/
│   └── db.py                   # SQLite helper + user/prediction CRUD
├── models/                     # model.pkl, vectorizer.pkl, metrics.json (generated)
├── templates/                   # HTML templates (Flask)
├── static/                      # CSS, JS, images
├── requirements.txt
├── Procfile
└── render.yaml
```

How it fits together: app.py wires routes and page rendering, predict.py loads the model artifacts and returns prediction + TF‑IDF based explanation, database/db.py stores users and prediction history, and services/report_generator.py composes PDF reports.

---

## How it works

1. User submits article text via the detector page or API.
2. Text → TF‑IDF vectorizer (vectorizer.pkl).
3. PassiveAggressiveClassifier (model.pkl) predicts label (0/1).
4. A confidence proxy is computed from the model's decision function.
5. Top TF‑IDF terms are extracted and returned as an explanation.
6. Prediction and metadata are saved to SQLite for the authenticated user.

---

## Getting started (local)

Prerequisites:
- Python 3.10+ (project uses 3.11 in config)
- Git

Clone and set up:

```bash
git clone https://github.com/Abhishekverma3205/TrusthLens.git
cd TrusthLens
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Required environment variables (recommended):
- SECRET_KEY — used by Flask sessions (default provided for development)
- FLASK_DEBUG — set to "1" to enable debug mode
- PORT — optional, used when running on a host

---

## Build the Model

If the trained artifacts are missing, create them with:

```bash
python bootstrap_model.py
```

This script:
- Loads data from `data/Fake.csv` and `data/True.csv` if present.
- If those CSVs are not present, it trains on built-in seed samples so the app works out of the box.
- Saves artifacts to:
  - `models/model.pkl`
  - `models/vectorizer.pkl`
  - `models/metrics.json`

Model metrics (accuracy, precision, recall, f1) are written to `models/metrics.json` and surfaced by the `/metrics` endpoint.

---

## Run the App

Development server:

```bash
python app.py
# then open http://127.0.0.1:5000
```

Production with Gunicorn (Procfile):

```procfile
web: gunicorn app:app --workers 2 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT
```

---

## Prediction API

POST /predict (authenticated session required)

Request body (JSON):

```json
{
  "news": "Your article text here..."
}
```

Response example:

```json
{
  "success": true,
  "prediction": "FAKE NEWS",
  "confidence": 96.42,
  "explanation": [
    {"word": "claim", "score": 0.321},
    {"word": "breaking", "score": 0.287}
  ]
}
```

cURL example (after logging in or with a valid cookie/session):

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"news":"Some text to classify"}' \
     http://127.0.0.1:5000/predict
```

Python example (requests):

```python
import requests
payload = {"news": "Some article text..."}
resp = requests.post("http://127.0.0.1:5000/predict", json=payload, cookies={'session': '<SESSION_COOKIE>'})
print(resp.json())
```

---

## Database & persistence

- SQLite DB located at `instance/truthlens.db` (created automatically).
- Tables:
  - users (id, full_name, username, email, password_hash, created_at)
  - predictions (id, user_id, news_text, prediction, confidence, created_at)
- Predictions are trimmed to 2000 chars when saved.
- Utility endpoints: `/dashboard-data` returns statistics and recent history.

---

## Deployment notes

- The app is configured for 12‑factor friendly hosts (see Procfile).
- For Render / Heroku: set SECRET_KEY and ensure `models/` contains the trained artifacts (or run bootstrap_model during build).
- `render.yaml` exists as an opinionated render configuration if you deploy on Render.

---

## Development & testing

- No automated tests included (yet). Add pytest, fixtures, and CI workflow for production readiness.
- Linting/formatting: add pre-commit configuration for black/isort/flake8 if desired.
- To iterate on the model: update `bootstrap_model.py` training/preprocessing, then re-run to regenerate artifacts.

---

## Contributing

Contributions are welcome. Suggested flow:
1. Fork the repository.
2. Create a feature branch: git checkout -b feat/your-feature
3. Make changes & add tests.
4. Open a pull request with a clear description and motivation.

Please include a short PR description explaining why the change improves the project.

---

## Security & privacy

- Passwords are hashed via Werkzeug's generate_password_hash.
- The model is a lightweight classifier and provides guidance — not definitive fact-checking.
- Do not store or share sensitive user content without appropriate consent. Consider adding data retention policies and encryption for production.

If you discover a security vulnerability, please open an issue labeled "security" or contact the repository owner directly.

---

## Future ideas

- Integrate external fact-check sources and citation links.
- Offer multiple model backends and model comparison UI.
- Add API authentication (API keys / OAuth) for external callers.
- Improve explanations using SHAP or attention-based attribution.
- Expand training data for better generalization.

---

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

Copyright (c) 2026 Abhishek verma

---

## Acknowledgements

Built with Flask, scikit-learn, and ReportLab. Seed dataset and model pipeline inspired by common TF‑IDF + linear classifier approaches for text classification.

---

Made to help people read news with more confidence and less noise.
