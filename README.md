
# AI Agent Backend

A **FastAPI-powered backend** for an AI assistant capable of chatting, sending Gmail emails, and creating Google Calendar events.
The backend is **modular**, **extensible**, and **ready for integration** with various frontends (web, desktop, mobile).

---

## 📌 Overview

This project provides a robust backend for an AI assistant with three main capabilities:

1. **Natural Language Chat** – Process user queries using an AI model.
2. **Gmail Integration** – Send emails programmatically after Google OAuth authentication.
3. **Google Calendar Integration** – Create events directly into a user’s calendar.

The backend uses **FastAPI** for speed and modern API design, with support for both **REST** and **WebSocket** interactions.
Authentication is handled using **Google OAuth 2.0**, and session state is maintained with a **SQLite** database.

---

## ✨ Features

### 🤖 Chat API

* REST endpoint (`POST /run`) to send text queries to the assistant.
* WebSocket endpoint (`/ws/{session_id}`) for real-time, streaming conversations.
* Uses session-based memory so the assistant can recall past messages.

### 🔐 Google OAuth

* Allows secure connection to Gmail & Calendar APIs.
* OAuth flow:

  1. User authorizes via Google.
  2. Backend stores refresh tokens.
  3. Subsequent API calls use the stored tokens.

### 📧 Gmail Integration

* Send formatted, AI-composed emails via the Gmail API.
* Helper functions for:

  * Email encoding (RFC 2822 format).
  * Draft creation and sending.

### 📅 Google Calendar Integration

* Create events directly into the user’s Google Calendar.
* Supports:

  * Event title, description, date/time.
  * Time zone support.

### 🧠 Session Memory

* Stores chat history per session in **SQLite**.
* Allows the assistant to maintain context between user queries.

---

## 📂 File Structure

| File / Folder        | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `main.py`            | Main FastAPI app with API endpoints.                         |
| `agent.py`           | AI assistant logic (calls the AI model).                     |
| `memory.py`          | Handles session memory and stores messages in SQLite.        |
| `gmail_calendar.py`  | Gmail and Calendar API integration.                          |
| `helpers.py`         | Utility functions (e.g., email formatting, base64 encoding). |
| `.env`               | Environment variables for API keys and secrets.              |
| `.gitignore`         | Files/folders excluded from version control.                 |
| `requirements.txt`   | Python dependencies.                                         |
| `google_tokens.json` | Stored Google OAuth tokens (generated at runtime).           |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/puneeth-hegde/Agentic-AI-Task-Automation-Bot
cd ai_agent
```

### 2️⃣ Create and Activate Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8000/oauth2callback
GOOGLE_TOKEN_FILE=google_tokens.json
```

> **Note:**
>
> * `GROQ_API_KEY` & `GROQ_MODEL` refer to the AI model provider you are using.
> * Google credentials can be obtained from the Google Cloud Console.
> * Make sure Gmail & Calendar APIs are enabled in your Google project.

### 5️⃣ Run the Backend Server

```sh
uvicorn main:app --reload --port 8000
```

Server runs at: `http://localhost:8000`

---

## 🚀 API Endpoints

### 🔹 Chat

* **`POST /run`**

  * **Request Body:** `{ "session_id": "abc123", "message": "Hello" }`
  * **Response:** AI assistant reply.

* **`WS /ws/{session_id}`**

  * Real-time chat with persistent session memory.

---

### 🔹 Google OAuth

* **`GET /authorize`**

  * Redirects to Google OAuth consent screen.

* **`GET /oauth2callback`**

  * Handles Google’s redirect and stores tokens.

* **`GET /auth_status`**

  * Checks if the user is authenticated.

---

### 🔹 Gmail

* **`POST /send_email`**

  * **Body:** `{ "to": "example@gmail.com", "subject": "Test", "body": "Hello!" }`
  * Sends an email via Gmail API.

---

### 🔹 Calendar

* **`POST /create_event`**

  * **Body:** `{ "summary": "Meeting", "start": "...", "end": "..." }`
  * Creates a Google Calendar event.

---

## 🛠 Development Notes

* CORS is enabled for frontend access.
* Uses SQLite for lightweight session storage.
* WebSocket chat allows real-time AI conversation.
* Any frontend (React, Vue, plain HTML/JS) can connect via WebSocket or REST.

---

## 🔒 Security Considerations

* Never commit `.env` or `google_tokens.json` to public repos.
* Tokens and API keys should be stored securely.
* Use HTTPS in production for secure OAuth flows.

---

## 📜 License

MIT License (or update accordingly).

---


