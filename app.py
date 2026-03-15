"""Flask entrypoint for AI-powered complaint management system."""
from __future__ import annotations

import os
import threading
import time

import schedule
from flask import Flask, jsonify, render_template, request

from analytics.analytics_service import get_dashboard_metrics
from database.db import init_db, session
from ml_models.train_model import train_model
from retraining.auto_retrainer import AutoRetrainer
from services.complaint_service import ComplaintService
from services.data_loader_service import DataLoaderService
from services.escalation_service import EscalationService
from services.query_service import QueryService

app = Flask(__name__)
complaint_service = ComplaintService()
query_service = QueryService()
retrainer = AutoRetrainer()


def bootstrap_system():
    init_db()

    model_path = os.path.join("ml_models", "model.pkl")
    if not os.path.exists(model_path):
        train_model()

    complaints_df = DataLoaderService.load_complaint_dataset()
    queries_df = DataLoaderService.load_query_dataset()

    complaint_service.classifier.load()
    query_service.model.train()

    with session() as conn:
        departments = sorted(set(complaints_df["department"].astype(str).tolist() + queries_df["department"].astype(str).tolist()))
        for dept in departments:
            conn.execute(
                "INSERT OR IGNORE INTO departments(name, senior_department) VALUES (?, ?)",
                (dept, f"Senior {dept}"),
            )


def scheduler_loop():
    schedule.every().hour.do(EscalationService.run_escalation_checks)
    schedule.every().week.do(lambda: retrainer.check_and_retrain(force=True))
    while True:
        schedule.run_pending()
        time.sleep(20)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/api/complaints", methods=["POST"])
def submit_complaint():
    payload = request.get_json(force=True)
    complaint_text = payload.get("text", "").strip()
    if not complaint_text:
        return jsonify({"error": "Complaint text is required."}), 400
    result = complaint_service.submit_complaint(complaint_text)
    return jsonify(result)


@app.route("/api/complaints", methods=["GET"])
def list_complaints():
    department = request.args.get("department")
    return jsonify(complaint_service.list_complaints(department))


@app.route("/api/complaints/<int:complaint_id>/resolve", methods=["POST"])
def resolve_complaint(complaint_id: int):
    payload = request.get_json(force=True)
    resolution = payload.get("resolution", "").strip()
    if not resolution:
        return jsonify({"error": "Resolution is required."}), 400
    complaint_service.resolve_complaint(complaint_id, resolution)
    retrain_state = retrainer.check_and_retrain(force=False)
    return jsonify({"message": "Complaint resolved.", "retraining": retrain_state})


@app.route("/api/query", methods=["POST"])
def answer_query():
    payload = request.get_json(force=True)
    question = payload.get("question", "").strip()
    if not question:
        return jsonify({"error": "Question is required."}), 400
    return jsonify(query_service.answer_query(question))


@app.route("/api/analytics", methods=["GET"])
def analytics_data():
    return jsonify(get_dashboard_metrics())


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    bootstrap_system()
    scheduler = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler.start()
    app.run(debug=True)
