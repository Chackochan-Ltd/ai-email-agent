import csv
from datetime import datetime

LOG_FILE = "data/logs.csv"

def log_action(email: str, intent: str, action: str):
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), intent, action, email[:50]])

def route_workflow(email: str, intent: str):
    if intent == "spam":
        log_action(email, intent, "ignored")
        return "Spam ignored"

    log_action(email, intent, "reply_generated")
    return "Reply drafted and logged"
