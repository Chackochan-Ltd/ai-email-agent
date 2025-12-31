import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------
# Fallback classifier
# ---------------------------
def fallback_classifier(email_text: str) -> dict:
    text = email_text.lower()

    if any(w in text for w in ["resume", "cv", "job", "apply", "position"]):
        return {
            "intent": "job",
            "confidence": 0.6,
            "reason": "Keyword-based fallback",
            "source": "fallback"
        }

    if any(w in text for w in ["help", "issue", "problem", "support", "error"]):
        return {
            "intent": "support",
            "confidence": 0.6,
            "reason": "Keyword-based fallback",
            "source": "fallback"
        }

    if any(w in text for w in ["win money", "free offer", "click here"]):
        return {
            "intent": "spam",
            "confidence": 0.7,
            "reason": "Spam phrase detected",
            "source": "fallback"
        }

    return {
        "intent": "query",
        "confidence": 0.5,
        "reason": "Default fallback",
        "source": "fallback"
    }

# ---------------------------
# Gemini classifier
# ---------------------------
def classify_intent(email_text: str) -> dict:
    try:
        prompt = f"""
Classify the following email into ONE of:
job, support, query, spam.

Respond ONLY in valid JSON with:
intent, confidence (0-1), reason.

Email:
{email_text}
"""

        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )

        result = json.loads(response.text.strip())
        result["source"] = "gemini"

        return result

    except Exception:
        return fallback_classifier(email_text)
