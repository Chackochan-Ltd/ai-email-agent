from gmail_reader import fetch_latest_emails
from gmail_sender import send_email
from intent_classifier import classify_intent
from reply_generator import generate_reply
from workflow_router import route_workflow

CONFIDENCE_THRESHOLD = 0.8


def run_agent():
    emails = fetch_latest_emails()

    if not emails:
        print("📭 No emails found.")
        return

    for mail in emails:
        email_body = mail["body"]
        sender = mail["from"]
        subject = mail["subject"]

        print("\n📩 New Email")
        print("From:", sender)
        print("Subject:", subject)

        # ---- AI Classification ----
        result = classify_intent(email_body)
        intent = result["intent"]
        confidence = result["confidence"]
        source = result.get("source", "unknown")

        print(f"🧠 Intent: {intent} | Confidence: {confidence} | Source: {source}")

        # ---- Spam Rule ----
        if intent == "spam":
            print("🚫 Spam detected — no reply sent")
            route_workflow(email_body, "spam")
            continue

        # ---- Generate Reply ----
        reply = generate_reply(intent, email_body)

        # ---- Confidence Gate ----
        if confidence >= CONFIDENCE_THRESHOLD:
            send_email(
                to_email=sender,
                subject=f"Re: {subject}",
                body=reply
            )
            print("✅ Reply auto-sent")
            route_workflow(email_body, intent)
        else:
            print("⏸️ Low confidence — reply held for manual review")
            route_workflow(email_body, "held_for_review")


if __name__ == "__main__":
    run_agent()
