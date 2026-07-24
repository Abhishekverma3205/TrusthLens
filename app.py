import os
from flask import (
    Flask, render_template, request, jsonify,
    redirect, url_for, session, flash, send_file
)

from predict import predict_news
from model_metrics import load_metrics
from services.report_generator import create_pdf
from database.db import (
    initialize_database, save_prediction, get_recent_predictions,
    get_statistics, create_user, verify_user, get_user_by_id,
    update_profile, change_password
)

# ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "truthlens-dev-key-change-in-production")

initialize_database()

# ─── Home ────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ─── Auth ────────────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success = create_user(
            request.form["full_name"].strip(),
            request.form["username"].strip(),
            request.form["email"].strip(),
            request.form["password"]
        )
        if success:
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        flash("Username or Email already exists.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = verify_user(
            request.form["username"].strip(),
            request.form["password"]
        )
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

# ─── Protected Pages ─────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/detector")
def detector():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("detector.html", username=session["username"])

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user  = get_user_by_id(session["user_id"])
    stats = get_statistics(session["user_id"])
    return render_template("profile.html", user=user, stats=stats)

# ─── Profile Actions ─────────────────────────────────────────

@app.route("/update-profile", methods=["POST"])
def update_user_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    update_profile(
        session["user_id"],
        request.form["full_name"].strip(),
        request.form["email"].strip()
    )
    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile"))

@app.route("/change-password", methods=["POST"])
def update_password():
    if "user_id" not in session:
        return redirect(url_for("login"))
    password = request.form["password"]
    if len(password) < 8:
        flash("Password must be at least 8 characters.", "danger")
        return redirect(url_for("profile"))
    change_password(session["user_id"], password)
    flash("Password updated successfully.", "success")
    return redirect(url_for("profile"))

# ─── AI Prediction API ───────────────────────────────────────

@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Please login first."}), 401
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request."}), 400
    news = data.get("news", "").strip()
    if len(news) < 20:
        return jsonify({"success": False, "message": "Please enter a longer article."})
    result = predict_news(news)
    save_prediction(session["user_id"], news, result["prediction"], result["confidence"])
    return jsonify({
        "success": True,
        "prediction":  result["prediction"],
        "confidence":  result["confidence"],
        "explanation": result.get("explanation", [])
    })

# ─── Download PDF ────────────────────────────────────────────

@app.route("/download-report", methods=["POST"])
def download_report():
    if "user_id" not in session:
        return redirect(url_for("login"))
    data = request.get_json()
    pdf  = create_pdf(
        data["news"], data["prediction"],
        data["confidence"], data["explanation"]
    )
    return send_file(
        pdf,
        as_attachment=True,
        download_name="TruthLens_Report.pdf",
        mimetype="application/pdf"
    )

# ─── Dashboard Data API ──────────────────────────────────────

@app.route("/dashboard-data")
def dashboard_data():
    if "user_id" not in session:
        return jsonify({"success": False}), 401
    stats   = get_statistics(session["user_id"])
    history = get_recent_predictions(session["user_id"])
    return jsonify({"success": True, "statistics": stats, "history": history})

@app.route("/metrics")
def metrics():
    if "user_id" not in session:
        return jsonify({"success": False}), 401
    return jsonify(load_metrics())

# ─── Errors ──────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

# ─── Health Check (Render) ───────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ─── Run ─────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
