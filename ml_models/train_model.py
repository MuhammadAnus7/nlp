"""Model training pipeline for complaint department classification."""
from __future__ import annotations

import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from services.data_loader_service import DataLoaderService

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "datasets" / "datas.xlsx"
MODEL_PATH = BASE_DIR / "ml_models" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "ml_models" / "vectorizer.pkl"


def preprocess_text(text: str) -> str:
    lowered = str(text).lower()
    cleaned = re.sub(r"[^a-z\s]", " ", lowered)
    tokens = [token for token in cleaned.split() if token and token not in ENGLISH_STOP_WORDS]
    return " ".join(tokens)


def train_model() -> None:
    print("Loading dataset")
    if DATA_PATH.exists():
        df = pd.read_excel(DATA_PATH)
    else:
        print("Dataset file missing; using fallback samples from DataLoaderService")
        df = DataLoaderService.load_complaint_dataset()
    required_columns = {"text", "department"}
    if not required_columns.issubset(df.columns):
        raise ValueError("datasets/datas.xlsx must contain columns: text, department")

    df = df.dropna(subset=["text", "department"])
    if df.empty:
        raise ValueError("Training dataset is empty after removing null rows.")

    x_train = df["text"].astype(str).apply(preprocess_text)
    y_train = df["department"].astype(str)

    print("Training model")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    x_vectors = vectorizer.fit_transform(x_train)

    model = LogisticRegression(max_iter=2000)
    model.fit(x_vectors, y_train)

    print("Saving model")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)


if __name__ == "__main__":
    train_model()
