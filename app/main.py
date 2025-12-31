from intent_classifier import classify_intent
from reply_generator import generate_reply
from workflow_router import route_workflow

# Mock incoming emails
EMAILS = [
    "Hi, I am applying for a job. Please find my resume attached.",
    "Hello, I need help with an issue on your platform.",
    "Congratulations! You won money. Click here."
]

def run_agent():
    for email in EMAILS:
        print("\n📩 New Email:", email)

        result = classify_intent(email)
        intent = result["intent"]

        print("🧠 Classified Intent:", intent)

        reply = generate_reply(intent, email)
        action = route_workflow(email, intent)

        if reply:
            print("✉️ Drafted Reply:", reply)

        print("⚙️ Action:", action)

if __name__ == "__main__":
    run_agent()
