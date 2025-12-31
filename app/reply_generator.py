import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

BASE_TEMPLATES = {
    "job": "Thank you for reaching out regarding career opportunities.",
    "support": "Thanks for contacting support regarding your issue.",
    "query": "Thank you for your message.",
    "spam": ""
}

def generate_reply(intent: str, email_text: str) -> str:
    if intent == "spam":
        return ""

    base_reply = BASE_TEMPLATES.get(
        intent,
        "Thank you for getting in touch."
    )

    try:
        prompt = f"""
Improve the following email reply.
Keep it professional and polite.
Do NOT add promises, timelines, or sensitive info.

Base reply:
{base_reply}

Original email:
{email_text}
"""

        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        return base_reply
