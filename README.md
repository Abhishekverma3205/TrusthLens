# TrusthLens

**TrusthLens** is a full-stack AI-powered fake news detection web application built with Flask. It lets users sign up, log in, analyze news articles, view prediction confidence and explanations, download PDF reports, and review their prediction history from a personal dashboard.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20App-6366f1?style=for-the-badge)](https://trusthlens.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge)](https://flask.palletsprojects.com/)

## Overview

TrusthLens classifies news content as **REAL NEWS** or **FAKE NEWS** using a trained text model and a TF-IDF vectorizer. The app is designed with a modern frontend and includes authentication, analytics, reporting, and a polished user experience.

## Key Features

- **AI news detection** with confidence score and word-level explanation
- **User authentication**: register, login, logout
- **Personal dashboard** with prediction history and analytics
- **Profile management**: update profile and change password
- **PDF report generation** for predictions
- **Usage metrics** and statistics dashboard
- **Responsive UI** with custom styling and interactive JavaScript
- **Health check endpoint** for deployment monitoring

## How It Works

1. A user submits a news article.
2. The article is vectorized using a trained **TF-IDF vectorizer**.
3. A **PassiveAggressiveClassifier** predicts whether the news is real or fake.
4. The app calculates a confidence score and extracts the most influential words.
5. The result is stored in the database and shown in the dashboard.

## Tech Stack

**Backend**
- Python
- Flask
- SQLite / local database layer
- scikit-learn
- pickle

**Frontend**
- HTML
- CSS
- JavaScript
- Bootstrap

**Deployment**
- Gunicorn
- Render

## Project Structure

```text
TrusthLens/
├── app.py
├── bootstrap_model.py
├── predict.py
├── model_metrics.py
├── services/
│   └── report_generator.py
├── database/
│   └── db.py
├── models/
│   ├── model.pkl
│   ├── vectorizer.pkl
│   └── metrics.json
├── templates/
├── static/
└── Procfile
```

## Requirements

- Python 3.11+
- pip
- A browser

## Installation

```bash
git clone https://github.com/Abhishekverma3205/TrusthLens.git
cd TrusthLens
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Model Setup

If the `models/` directory does not already contain the trained artifacts, generate them with:

```bash
python bootstrap_model.py
```

This script will:
- train the news classifier,
- save `model.pkl` and `vectorizer.pkl`,
- write evaluation metrics to `models/metrics.json`.

## Running Locally

```bash
python app.py
```

By default, the app runs on:

```text
http://127.0.0.1:5000
```

## Deployment

The repository includes a `Procfile` for Gunicorn-based deployment:

```procfile
web: gunicorn app:app --workers 2 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT
```

## Main Routes

- `/` — Home page
- `/about` — About page
- `/register` — Create account
- `/login` — Sign in
- `/dashboard` — User dashboard
- `/detector` — News detection page
- `/profile` — User profile
- `/predict` — Prediction API
- `/download-report` — PDF report download
- `/dashboard-data` — Dashboard statistics
- `/metrics` — Model metrics
- `/health` — Health check

## Prediction API

### Request

`POST /predict`

```json
{
  "news": "Your article text here..."
}
```

### Response

```json
{
  "success": true,
  "prediction": "FAKE NEWS",
  "confidence": 96.42,
  "explanation": [
    { "word": "claim", "score": 0.321 },
    { "word": "breaking", "score": 0.287 }
  ]
}
```

## Metrics

The model metrics are saved after training and exposed in the dashboard:

- Accuracy
- Precision
- Recall
- F1 score

## Notes

- `bootstrap_model.py` can train on bundled seed data if no CSV dataset is present.
- `predict.py` loads the trained model artifacts from `models/` on startup.
- The app uses session-based authentication for protected routes.

## Future Improvements

- Add more training data for stronger detection accuracy
- Support multiple model types and A/B testing
- Add article source verification and fact-checking links
- Improve explainability with richer NLP insights
- Add API authentication for external clients

## License

No license has been specified in this repository.

---

Built for trustworthy news analysis and a clean user experience.
