"""Service for user query answering."""
from database.db import session
from ml_models.query_engine import QueryEngine
from services.log_service import log_event


class QueryService:
    def __init__(self):
        self.model = QueryEngine()

    def answer_query(self, question: str):
        result = self.model.answer(question)
        with session() as conn:
            cur = conn.execute(
                "INSERT INTO queries(question, predicted_answer, matched_department, similarity_score) VALUES (?, ?, ?, ?)",
                (question, result["answer"], result["department"], result["score"]),
            )
            query_id = cur.lastrowid
        log_event("QUERY_ANSWERED", f"Query #{query_id} processed", {"score": result["score"]})
        result["id"] = query_id
        return result
