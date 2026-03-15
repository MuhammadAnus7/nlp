"""Complaint classification using TF-IDF + Logistic Regression with spaCy preprocessing."""
from __future__ import annotations

from dataclasses import dataclass
import joblib
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from services.data_loader_service import DataLoaderService
from utils.config import MODEL_DIR


@dataclass
class PredictionResult:
    department: str
    confidence: float


class ComplaintClassifier:
    def __init__(self):
        self.model_path = MODEL_DIR / "complaint_classifier.joblib"
        self.nlp = spacy.blank("en")
        self.pipeline: Pipeline | None = None

    def preprocess(self, text: str) -> str:
        doc = self.nlp(text.lower())
        tokens = [t.text for t in doc if not t.is_stop and t.is_alpha]
        return " ".join(tokens) if tokens else text.lower()

    def train(self):
        df = DataLoaderService.load_complaint_dataset()
        x = df["text"].astype(str).apply(self.preprocess)
        y = df["department"].astype(str)
        self.pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                ("clf", LogisticRegression(max_iter=1500)),
            ]
        )
        self.pipeline.fit(x, y)
        joblib.dump(self.pipeline, self.model_path)

    def load_or_train(self):
        if self.model_path.exists():
            self.pipeline = joblib.load(self.model_path)
        else:
            self.train()

    def predict(self, text: str) -> PredictionResult:
        if self.pipeline is None:
            self.load_or_train()
        processed = self.preprocess(text)
        proba = self.pipeline.predict_proba([processed])[0]
        idx = proba.argmax()
        label = self.pipeline.classes_[idx]
        return PredictionResult(department=label, confidence=float(proba[idx]))
