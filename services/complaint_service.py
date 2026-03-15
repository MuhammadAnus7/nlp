"""Service for complaint intake, routing, and resolution."""
from __future__ import annotations

from database.db import session
from ml_models.complaint_classifier import ComplaintClassifier
from ml_models.sentiment_analyzer import SentimentAnalyzer
from services.log_service import log_event
from services.priority_service import PriorityService


class ComplaintService:
    def __init__(self):
        self.classifier = ComplaintClassifier()
        self.sentiment = SentimentAnalyzer()

    def submit_complaint(self, text: str):
        dept_pred = self.classifier.predict(text)
        sentiment = self.sentiment.analyze(text)
        priority = PriorityService.detect_priority(text, sentiment["score"])

        with session() as conn:
            cur = conn.execute(
                """
                INSERT INTO complaints(complaint_text, department, priority, sentiment_score, sentiment_label, status)
                VALUES (?, ?, ?, ?, ?, 'OPEN')
                """,
                (text, dept_pred.department, priority, sentiment["score"], sentiment["label"]),
            )
            complaint_id = cur.lastrowid

        log_event("COMPLAINT_SUBMITTED", f"Complaint #{complaint_id} submitted", {"department": dept_pred.department})
        return {
            "id": complaint_id,
            "department": dept_pred.department,
            "priority": priority,
            "sentiment": sentiment,
            "confidence": dept_pred.confidence,
        }

    def list_complaints(self, department: str | None = None):
        query = "SELECT * FROM complaints"
        params = []
        if department:
            query += " WHERE department = ?"
            params.append(department)
        query += " ORDER BY created_at DESC"
        with session() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]

    def resolve_complaint(self, complaint_id: int, resolution_text: str):
        with session() as conn:
            conn.execute(
                """
                UPDATE complaints
                SET status='RESOLVED', resolution_text=?, resolved_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
                """,
                (resolution_text, complaint_id),
            )
            row = conn.execute("SELECT complaint_text, department FROM complaints WHERE id=?", (complaint_id,)).fetchone()
            if row:
                conn.execute(
                    "INSERT INTO retraining_queue(source_type, source_id, text, department) VALUES ('complaint', ?, ?, ?)",
                    (complaint_id, row["complaint_text"], row["department"]),
                )
        log_event("COMPLAINT_RESOLVED", f"Complaint #{complaint_id} resolved")
