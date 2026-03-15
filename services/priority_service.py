"""Priority detection combining keyword rules and sentiment."""
from utils.config import URGENT_KEYWORDS


class PriorityService:
    @staticmethod
    def detect_priority(text: str, sentiment_score: float) -> str:
        lowered = text.lower()
        if any(k in lowered for k in URGENT_KEYWORDS):
            return "HIGH"
        if sentiment_score <= -0.35:
            return "HIGH"
        if sentiment_score >= 0.2:
            return "LOW"
        return "NORMAL"
