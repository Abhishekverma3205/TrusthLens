import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "instance", "truthlens.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            news_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ─── User Management ───────────────────────────────────────────

def create_user(full_name, username, email, password):
    try:
        conn = get_connection()
        hashed = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (full_name, username, email, password) VALUES (?, ?, ?, ?)",
            (full_name, username, email, hashed)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(username, password):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if user and check_password_hash(user["password"], password):
        return dict(user)
    return None


def get_user_by_id(user_id):
    conn = get_connection()
    user = conn.execute(
        "SELECT id, full_name, username, email, created_at FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def update_profile(user_id, full_name, email):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
        (full_name, email, user_id)
    )
    conn.commit()
    conn.close()


def change_password(user_id, new_password):
    conn = get_connection()
    hashed = generate_password_hash(new_password)
    conn.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hashed, user_id)
    )
    conn.commit()
    conn.close()


# ─── Predictions ───────────────────────────────────────────────

def save_prediction(user_id, news_text, prediction, confidence):
    conn = get_connection()
    conn.execute(
        "INSERT INTO predictions (user_id, news_text, prediction, confidence) VALUES (?, ?, ?, ?)",
        (user_id, news_text[:2000], prediction, confidence)
    )
    conn.commit()
    conn.close()


def get_recent_predictions(user_id, limit=20):
    conn = get_connection()
    rows = conn.execute(
        """SELECT id, prediction, confidence,
           substr(news_text, 1, 120) as preview,
           created_at
           FROM predictions
           WHERE user_id = ?
           ORDER BY created_at DESC
           LIMIT ?""",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_statistics(user_id):
    conn = get_connection()

    total = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ?",
        (user_id,)
    ).fetchone()["cnt"]

    fake = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ? AND prediction = 'FAKE NEWS'",
        (user_id,)
    ).fetchone()["cnt"]

    real = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ? AND prediction = 'REAL NEWS'",
        (user_id,)
    ).fetchone()["cnt"]

    avg_conf = conn.execute(
        "SELECT AVG(confidence) as avg FROM predictions WHERE user_id = ?",
        (user_id,)
    ).fetchone()["avg"]

    # Daily counts for last 7 days
    daily = conn.execute(
        """SELECT date(created_at) as day, COUNT(*) as cnt
           FROM predictions
           WHERE user_id = ? AND created_at >= date('now', '-7 days')
           GROUP BY day
           ORDER BY day ASC""",
        (user_id,)
    ).fetchall()

    conn.close()

    return {
        "total": total,
        "fake": fake,
        "real": real,
        "avg_confidence": round(avg_conf or 0, 2),
        "daily": [dict(d) for d in daily]
    }
