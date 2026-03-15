"""Semantic query answering with sentence-transformer similarity search."""
from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from services.data_loader_service import DataLoaderService
from utils.config import SIMILARITY_THRESHOLD


class QueryEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.df = None
        self.embeddings = None

    def train(self) -> None:
        self.df = DataLoaderService.load_query_dataset().reset_index(drop=True)
        questions = self.df["question"].astype(str).tolist()
        self.embeddings = self.model.encode(questions, normalize_embeddings=True)

    def ensure_ready(self) -> None:
        if self.df is None or self.embeddings is None:
            self.train()

    def answer(self, question: str) -> dict:
        self.ensure_ready()
        query_embedding = self.model.encode([question], normalize_embeddings=True)[0]
        scores = np.dot(self.embeddings, query_embedding)
        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])
        best_match = self.df.iloc[best_index]

        if best_score < SIMILARITY_THRESHOLD:
            return {
                "answer": "Sorry, no relevant answer found.",
                "department": "Unknown",
                "score": best_score,
            }

        return {
            "answer": str(best_match["answer"]),
            "department": str(best_match["department"]),
            "score": best_score,
        }
