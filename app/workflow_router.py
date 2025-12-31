import csv
import os
from datetime import datetime

LOG_FILE = "data/logs.csv"


def _ensure_log_file():
    """Create log file with headers if it doesn't exist."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "intent",
                "action",
                "email_preview"
            ])


def route_workflow(email_text: str, intent: str):
    """
    Logs the workflow decision.
    intent can be:
    - job
    - support
    - query
    - spam
    - held_for_review
    """
    _ensure_log_file()

    if intent == "spam":
        action = "ignored"
    elif intent == "held_for_review":
        action = "held_for_review"
    else:
        action = "auto_replied"

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            intent,
            action,
            email_text[:80].replace("\n", " ")
        ])
