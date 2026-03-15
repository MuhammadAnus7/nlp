"""Sentiment analysis helpers using TextBlob and VADER."""
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentModel:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> dict:
        blob_polarity = TextBlob(text).sentiment.polarity
        vader_score = self.vader.polarity_scores(text)["compound"]
        blended = (blob_polarity + vader_score) / 2

        if blended < -0.35:
            label = "NEGATIVE"
        elif blended > 0.25:
            label = "POSITIVE"
        else:
            label = "NEUTRAL"

        return {
            "score": blended,
            "label": label,
            "blob": blob_polarity,
            "vader": vader_score,
        }
