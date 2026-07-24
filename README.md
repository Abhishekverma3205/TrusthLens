# TrusthLens

> **Spot misinformation. Understand why. Share confidence.**

**TrusthLens** is a sleek, AI-powered fake news detector that turns any article into a fast, readable verdict: **REAL NEWS** or **FAKE NEWS**. It blends a trained NLP model, a polished dashboard, user accounts, and downloadable reports into one clean experience.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-6366f1?style=for-the-badge)](https://trusthlens.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Model-f7931e?style=for-the-badge)](https://scikit-learn.org/)

## Why TrusthLens?

News moves fast. So does misinformation. TrusthLens helps users quickly check a story, see the model’s confidence, and inspect the words that influenced the prediction.

It’s not just a classifier — it’s an experience.

## Highlights

- **Instant news verdicts** with confidence scoring
- **Explainable AI** with word-level TF-IDF insights
- **Secure user accounts** with registration and login
- **Personal dashboard** with history and analytics
- **Profile controls** for updating account details and password
- **PDF report generation** for sharing results
- **Modern responsive UI** built with HTML, CSS, and JavaScript
- **Deployment-ready** with Gunicorn and Render

## How It Works

```text
Paste article → Vectorize text → Predict real/fake → Explain result → Save history → Download report
```

1. A user submits a news article.
2. The text is transformed using a **TF-IDF vectorizer**.
3. A **PassiveAggressiveClassifier** predicts whether it is real or fake.
4. The app returns a confidence score and the most important keywords.
5. The prediction is stored and displayed in the dashboard.

## Tech Stack

**Backend**
- Python
- Flask
- scikit-learn
- pickle
- SQLite/local database layer

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

## Getting Started

```bash
git clone https://github.com/Abhishekverma3205/TrusthLens.git
cd TrusthLens
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Build the Model

If the trained artifacts are missing, generate them with:

```bash
python bootstrap_model.py
```

This will:
- train the classifier,
- save `models/model.pkl`,
- save `models/vectorizer.pkl`,
- write metrics to `models/metrics.json`.

## Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deployment

The app is configured for Gunicorn via `Procfile`:

```procfile
web: gunicorn app:app --workers 2 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT
```

## Main Routes

- `/` — Home
- `/about` — About
- `/register` — Create account
- `/login` — Sign in
- `/dashboard` — User dashboard
- `/detector` — News detector
- `/profile` — Profile page
- `/predict` — Prediction API
- `/download-report` — PDF report download
- `/dashboard-data` — Dashboard analytics
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

## Model Metrics

The dashboard exposes key evaluation scores:

- Accuracy
- Precision
- Recall
- F1 score

## What Makes It Stand Out

- Clear and intuitive UI
- Fast prediction pipeline
- Built-in explainability
- User-specific saved history
- Shareable PDF reports

## Future Ideas

- Add more training data for stronger accuracy
- Support multiple models and comparisons
- Add fact-check links and source verification
- Improve explanations with richer NLP
- Add API authentication for external use

## License

No license has been specified yet.

---

Made to help people read news with more confidence and less noise.
