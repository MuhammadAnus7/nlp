"""Semantic query answering using SentenceTransformers cosine similarity."""
from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from services.data_loader_service import DataLoaderService
from utils.config import SIMILARITY_THRESHOLD


class QueryAnsweringModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.df = None
        self.embeddings = None

    def train(self):
        self.df = DataLoaderService.load_query_dataset().reset_index(drop=True)
        self.embeddings = self.model.encode(self.df["question"].astype(str).tolist(), normalize_embeddings=True)

    def ensure_ready(self):
        if self.df is None or self.embeddings is None:
            self.train()

    def answer(self, question: str):
        self.ensure_ready()
        q_vec = self.model.encode([question], normalize_embeddings=True)[0]
        scores = np.dot(self.embeddings, q_vec)
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])
        row = self.df.iloc[best_idx]

        if best_score < SIMILARITY_THRESHOLD:
            return {
                "answer": "Sorry, no relevant answer found.",
                "department": "Unknown",
                "score": best_score,
            }

        return {
            "answer": row["answer"],
            "department": row["department"],
            "score": best_score,
        }
