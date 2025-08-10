import uuid
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from agent import AssistantAgent
from memory import init_db, add_message, get_history
from gmail_calendar import get_auth_url, exchange_code_for_tokens, load_credentials, send_gmail_message, create_calendar_event
from helpers import build_rfc2822_message, encode_message_base64url

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()
agent = AssistantAgent()

class RunRequest(BaseModel):
    session_id: str | None = None
    query: str

class SendEmailRequest(BaseModel):
    session_id: str | None = None
    sender: str
    to: str
    subject: str
    body: str
    cc: str | None = None
    bcc: str | None = None

class CreateEventRequest(BaseModel):
    session_id: str | None = None
    event: dict

@app.post("/run")
async def run_task(req: RunRequest):
    session_id = req.session_id or str(uuid.uuid4())
    query = req.query
    add_message(session_id, "user", query)
    result = agent.run(query)
    add_message(session_id, "assistant", str(result))
    return {"session_id": session_id, "result": result}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("query")
            add_message(session_id, "user", query)
            result = agent.run(query)
            add_message(session_id, "assistant", str(result))
            await websocket.send_json({"result": result})
    except WebSocketDisconnect:
        print("Client disconnected")

# Google OAuth endpoints
@app.get("/authorize")
def authorize():
    try:
        url = get_auth_url()
        return RedirectResponse(url)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return HTMLResponse("No code returned in request", status_code=400)
    try:
        creds = exchange_code_for_tokens(code)
        return HTMLResponse("Authorization complete. You can close this tab and return to the assistant.")
    except Exception as e:
        return HTMLResponse(f"Authorization failed: {e}", status_code=500)

@app.get("/auth_status")
def auth_status():
    creds = load_credentials()
    return {"authorized": bool(creds)}

@app.post("/send_email")
def send_email(req: SendEmailRequest):
    # requires Google credentials
    session_id = req.session_id or str(uuid.uuid4())
    add_message(session_id, "user", f"send_email: to={req.to} subject={req.subject}")
    creds = load_credentials()
    if not creds:
        return JSONResponse({"error":"Google not authorized. Visit /authorize"}, status_code=401)
    # Build message and send
    rfc = build_rfc2822_message(req.sender, req.to, req.subject, req.body, cc=req.cc, bcc=req.bcc)
    encoded = encode_message_base64url(rfc)
    try:
        resp = send_gmail_message(encoded)
        add_message(session_id, "assistant", f"email_sent: {resp}")
        return {"status":"sent", "response": resp}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/create_event")
def create_event(req: CreateEventRequest):
    session_id = req.session_id or str(uuid.uuid4())
    add_message(session_id, "user", f"create_event: {req.event}")
    creds = load_credentials()
    if not creds:
        return JSONResponse({"error":"Google not authorized. Visit /authorize"}, status_code=401)
    try:
        created = create_calendar_event(req.event)
        add_message(session_id, "assistant", f"event_created: {created.get('id')}")
        return {"status":"created", "event": created}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
        return JSONResponse({"error": str(e)}, status_code=500)
