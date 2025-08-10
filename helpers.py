# helpers.py
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def build_rfc2822_message(sender, to, subject, body, cc=None, bcc=None):
    """
    Build a simple RFC 2822 formatted email message.
    """
    headers = [
        f"From: {sender}",
        f"To: {to}",
        f"Subject: {subject}",
    ]
    if cc:
        headers.append(f"Cc: {cc}")
    if bcc:
        headers.append(f"Bcc: {bcc}")
    headers.append("")  # blank line between headers and body
    headers.append(body)
    return "\r\n".join(headers)

def encode_message_base64url(rfc2822_str: str) -> str:
    """
    Encode RFC 2822 message string into base64url format expected by Gmail API.
    """
    raw_bytes = rfc2822_str.encode("utf-8")
    encoded = base64.urlsafe_b64encode(raw_bytes).decode("utf-8")
    # Gmail accepts the urlsafe base64 with padding; it's fine to leave padding.
    return encoded
