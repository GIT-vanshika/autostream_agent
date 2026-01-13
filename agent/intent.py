from typing import Literal
from agent.state import IntentType


def classify_intent(user_text: str) -> IntentType:
    text = user_text.lower()

    greeting_words = ["hi", "hello", "hey", "namaste"]
    high_intent_phrases = [
        "buy",
        "purchase",
        "subscribe",
        "upgrade",
        "get started",
        "sign up",
        "take a trial",
        "start trial",
    ]

    if any(w in text for w in greeting_words):
        return "greeting"

    if any(p in text for p in high_intent_phrases):
        return "high_intent"

    product_keywords = [
        "price",
        "pricing",
        "plan",
        "feature",
        "limit",
        "policy",
        "refund",
        "support",
        "platform",
    ]
    if any(k in text for k in product_keywords):
        return "product_query"

    return "unknown"
