"""Automatic model retraining logic with version tracking."""
from __future__ import annotations

from datetime import datetime
from database.db import session
from ml_models.complaint_classifier import ComplaintClassifier
from services.log_service import log_event
from utils.config import RETRAIN_RECORD_THRESHOLD


class AutoRetrainer:
    def __init__(self):
        self.classifier = ComplaintClassifier()

    def check_and_retrain(self, force: bool = False):
        with session() as conn:
            count = conn.execute("SELECT COUNT(*) AS c FROM retraining_queue").fetchone()["c"]
        if not force and count < RETRAIN_RECORD_THRESHOLD:
            return {"retrained": False, "queued_records": count}

        self.classifier.train()
        version_tag = datetime.utcnow().strftime("v%Y%m%d%H%M%S")
        with session() as conn:
            conn.execute(
                "INSERT INTO model_versions(model_name, version_tag, trained_on_records, metrics) VALUES (?, ?, ?, ?)",
                ("complaint_classifier", version_tag, count, "{}"),
            )
            conn.execute("DELETE FROM retraining_queue")
        log_event("MODEL_RETRAINED", "Complaint classifier retrained", {"version": version_tag, "records": count})
        return {"retrained": True, "version": version_tag, "records": count}
