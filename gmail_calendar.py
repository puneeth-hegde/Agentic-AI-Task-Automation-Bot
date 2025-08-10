# gmail_calendar.py
import base64

def get_auth_url():
    # TODO: Implement actual logic
    return "https://accounts.google.com/o/oauth2/auth"

def exchange_code_for_tokens(code):
    # TODO: Implement actual logic
    return {"access_token": "dummy_token"}

def load_credentials():
    # TODO: Implement actual logic
    return {"access_token": "dummy_token"}

def send_gmail_message(encoded_message):
    # TODO: Implement actual logic
    return {"id": "dummy_email_id"}

def create_calendar_event(event):
    # TODO: Implement actual logic
    return {"id": "dummy_event_id"}

def encode_message_base64url(rfc2822_str: str) -> str:
    """
    Encode RFC 2822 message string into base64url format expected by Gmail API.
    """
    raw_bytes = rfc2822_str.encode("utf-8")
    encoded = base64.urlsafe_b64encode(raw_bytes).decode("utf-8")
    # Gmail accepts the urlsafe base64 with padding; it's fine to leave padding.
    return encoded
