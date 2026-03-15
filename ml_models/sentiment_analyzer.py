"""Sentiment analysis module using TextBlob + VADER."""
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> dict:
        blob_score = TextBlob(text).sentiment.polarity
        vader_score = self.vader.polarity_scores(text)["compound"]
        score = (blob_score + vader_score) / 2

        if score > 0.25:
            label = "positive"
        elif score < -0.35:
            label = "negative"
        else:
            label = "neutral"

        return {
            "score": score,
            "label": label,
            "blob": blob_score,
            "vader": vader_score,
        }
