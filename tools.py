# tools.py
import re
from typing import Dict

def draft_email_tool(input_data):
    """
    input_data: dict or str -> returns formatted email text.
    """
    if isinstance(input_data, str):
        recipient = "[Recipient]"
        subject = "Follow-up"
        body_points = [input_data]
        signature = "Your Name"
    else:
        recipient = input_data.get("recipient", "[Recipient]")
        subject = input_data.get("subject", "Follow-up")
        body_points = input_data.get("points", ["Following up on our previous discussion."])
        signature = input_data.get("signature", "Your Name")
    body = "\n\n".join(body_points) if isinstance(body_points, (list, tuple)) else str(body_points)
    email_text = f"Subject: {subject}\n\nDear {recipient},\n\n{body}\n\nBest regards,\n{signature}"
    return email_text

def extract_data_tool(text: str):
    """
    Extract monetary values and general numbers from a text string.
    Returns dict {money: [...], numbers:[...], raw: text}
    """
    # money like $1,234.56
    money = re.findall(r'\$\s*[\d,]+(?:\.\d+)?', text)
    # numbers not preceded by $
    numbers = re.findall(r'(?<!\$)\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)
    money_clean = [m.replace("$", "").replace(" ", "").replace(",", "") for m in money]
    numbers_clean = [n.replace(",", "") for n in numbers]
    return {"money": money_clean, "numbers": numbers_clean, "raw": text}

def generate_report_tool(data):
    """
    Summarizes a dict or text into a small report text
    """
    if isinstance(data, dict):
        summary = ["Report Summary:"]
        for k, v in data.items():
            summary.append(f"- {k}: {v}")
        return "\n".join(summary)
    else:
        return f"Report Summary:\nPreview: {str(data)[:1000]}"

def create_calendar_event_tool(event):
    """
    Stub: returns event metadata. Replace with Google Calendar call after OAuth.
    event: dict {title, start, end, timezone, attendees}
    """
    return {"event_id": "evt_local_stub_001", "status": "created_stub", **(event or {})}
