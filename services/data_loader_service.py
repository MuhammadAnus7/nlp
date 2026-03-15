"""Load and validate excel datasets used by ML modules."""
from __future__ import annotations

import pandas as pd
from utils.config import DATA_FILE, QUERY_FILE


class DataLoaderService:
    @staticmethod
    def load_complaint_dataset() -> pd.DataFrame:
        if DATA_FILE.exists():
            df = pd.read_excel(DATA_FILE)
        else:
            df = pd.DataFrame(
                [
                    {"text": "Teacher absent frequently", "department": "Academics"},
                    {"text": "School fees receipt issue", "department": "Finance"},
                ]
            )
        expected = {"text", "department"}
        if not expected.issubset(df.columns):
            raise ValueError(f"datas.xlsx must contain columns: {expected}")
        return df.dropna(subset=["text", "department"])

    @staticmethod
    def load_query_dataset() -> pd.DataFrame:
        if QUERY_FILE.exists():
            df = pd.read_excel(QUERY_FILE)
        else:
            df = pd.DataFrame(
                [
                    {
                        "question": "How can I apply for admission?",
                        "answer": "Please visit the nearest campus with required documents.",
                        "department": "Admissions",
                    }
                ]
            )
        expected = {"question", "answer", "department"}
        if not expected.issubset(df.columns):
            raise ValueError(f"queries.xlsx must contain columns: {expected}")
        return df.dropna(subset=["question", "answer", "department"])
