import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import pickle
import os

def get_gmail_service():
    with open("token.json", "rb") as token:
        creds = pickle.load(token)

    return build("gmail", "v1", credentials=creds)

def send_email(to_email: str, subject: str, body: str):
    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()
