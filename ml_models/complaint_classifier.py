"""Complaint classifier that loads persisted model artifacts."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from ml_models.train_model import train_model


@dataclass
class PredictionResult:
    department: str
    confidence: float


class ComplaintClassifier:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        self.model_path = base_dir / "model.pkl"
        self.vectorizer_path = base_dir / "vectorizer.pkl"
        self.model = None
        self.vectorizer = None

    @staticmethod
    def preprocess(text: str) -> str:
        lowered = str(text).lower()
        cleaned = re.sub(r"[^a-z\s]", " ", lowered)
        tokens = [token for token in cleaned.split() if token and token not in ENGLISH_STOP_WORDS]
        return " ".join(tokens)

    def load(self) -> None:
        if not self.model_path.exists() or not self.vectorizer_path.exists():
            train_model()
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    def predict_department(self, text: str) -> str:
        if self.model is None or self.vectorizer is None:
            self.load()
        processed = self.preprocess(text)
        features = self.vectorizer.transform([processed])
        return str(self.model.predict(features)[0])

    def predict(self, text: str) -> PredictionResult:
        if self.model is None or self.vectorizer is None:
            self.load()
        processed = self.preprocess(text)
        features = self.vectorizer.transform([processed])
        department = str(self.model.predict(features)[0])
        confidence = 1.0
        if hasattr(self.model, "predict_proba"):
            confidence = float(self.model.predict_proba(features)[0].max())
        return PredictionResult(department=department, confidence=confidence)

    def train(self) -> None:
        train_model()
        self.load()
