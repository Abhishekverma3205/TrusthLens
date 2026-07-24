# 🧠 TruthLens AI — Fake News Detector

A full-stack AI-powered fake news detection web app built with Flask, scikit-learn, and a dark glassmorphism UI.

---

## 🚀 Deploy on Render (Free)

### One-click method
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**

### Manual setup on Render
| Field | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python bootstrap_model.py` |
| **Start Command** | `gunicorn app:app --workers 2 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT` |
| **Environment Variables** | `SECRET_KEY` = (generate a long random string) |

> **Disk:** Add a 1 GB disk mounted at `/opt/render/project/src/instance` to persist the SQLite database across deploys.

---

## 🏃 Run Locally

```bash
# 1. Clone & enter project
git clone <your-repo-url>
cd TruthLens_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model
#    Option A — with real dataset (place Fake.csv + True.csv in data/)
python bootstrap_model.py
#    Option B — bootstrap without dataset (auto seed samples)
python bootstrap_model.py

# 5. Run the app
python app.py
```

Open → http://localhost:5000

---

## 📂 Project Structure

```
TruthLens_project/
├── app.py                    # Flask application (all routes)
├── predict.py                # ML prediction logic
├── model_metrics.py          # Load saved metrics JSON
├── bootstrap_model.py        # Train & save model (run once)
├── train_model.py            # Full trainer (requires Fake.csv/True.csv)
│
├── database/
│   └── db.py                 # SQLite helpers (users, predictions)
│
├── services/
│   └── report_generator.py   # PDF report via ReportLab
│
├── models/                   # Auto-created by bootstrap_model.py
│   ├── model.pkl
│   ├── vectorizer.pkl
│   └── metrics.json
│
├── data/                     # Place Fake.csv + True.csv here
├── instance/                 # Auto-created — holds SQLite DB
│
├── templates/                # Jinja2 HTML templates
│   ├── index.html
│   ├── about.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── detector.html
│   ├── profile.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/                  # Dark glassmorphism styles
│   └── js/                   # Dashboard, detector, auth JS
│
├── Procfile                  # Gunicorn start command
├── render.yaml               # Render deploy config
├── runtime.txt               # Python 3.11.9
└── requirements.txt          # Pinned production dependencies
```

---

## 🤖 ML Model

| Component | Detail |
|---|---|
| Algorithm | PassiveAggressiveClassifier |
| Features | TF-IDF (max 50k features, English stopwords) |
| Dataset | ISOT Fake News Dataset (Fake.csv + True.csv) |
| Accuracy | ~99% on ISOT dataset |
| Explainability | Top TF-IDF keyword scores per prediction |

To use the full ISOT dataset:
1. Download from [Kaggle — Fake News Detection](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset)
2. Place `Fake.csv` and `True.csv` in the `data/` folder
3. Run `python bootstrap_model.py`

---

## ✅ Completed Phases

| Phase | Feature |
|---|---|
| 1 | Frontend — glassmorphism UI, responsive, animations |
| 2 | ML — TF-IDF + PAC model, confidence score, explainability |
| 3 | Backend — Flask routes, REST APIs |
| 4 | Authentication — register, login, logout, sessions |
| 5 | Explainable AI — keyword scores, PDF report download |
| 6 | Dashboard — prediction history, charts, statistics |
| 7 | Deployment — Render-ready, Gunicorn, env vars, health check |

---

## 🔑 Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask session secret | auto-generated on Render |
| `FLASK_DEBUG` | Enable debug mode | `0` |
| `PORT` | Server port | `5000` |

---

## 📡 API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/` | — | Landing page |
| GET | `/about` | — | About page |
| POST | `/register` | — | Create account |
| POST | `/login` | — | Login |
| GET | `/logout` | ✓ | Logout |
| GET | `/dashboard` | ✓ | Dashboard page |
| GET | `/detector` | ✓ | Detector page |
| GET | `/profile` | ✓ | Profile page |
| POST | `/predict` | ✓ | Run AI prediction |
| GET | `/dashboard-data` | ✓ | Stats + history JSON |
| GET | `/metrics` | ✓ | Model accuracy JSON |
| POST | `/download-report` | ✓ | Download PDF |
| GET | `/health` | — | Health check |
"# TrusthLens" 
