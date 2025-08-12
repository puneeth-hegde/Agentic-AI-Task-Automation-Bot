# AI Agent Backend

This project is a FastAPI-based backend for an AI assistant that supports chat, Gmail integration, and Google Calendar event creation. It is designed to be extensible and can be connected to various frontends.

## Features

- **Chat API**: Interact with an AI assistant via REST or WebSocket.
- **Google OAuth**: Authorize with Google to send emails and create calendar events.
- **Gmail Integration**: Send emails using the Gmail API.
- **Google Calendar Integration**: Create calendar events using the Calendar API.
- **Session Memory**: Stores conversation history per session.

## File Structure

- `main.py`: FastAPI app with all API endpoints.
- `agent.py`: Defines the assistant agent logic.
- `memory.py`: Handles session memory and message history.
- `gmail_calendar.py`: Integrates with Gmail and Google Calendar APIs.
- `helpers.py`: Utility functions for email formatting and encoding.
- `.env`: Stores API keys and secrets.
- `.gitignore`: Ignores virtual environment, frontend, and other files.

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd ai_agent
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file with your API keys and Google OAuth credentials:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8000/oauth2callback
GOOGLE_TOKEN_FILE=google_tokens.json
```

### 5. Run the Backend Server

```sh
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `POST /run`: Run a chat query with the assistant.
- `GET /authorize`: Start Google OAuth flow.
- `GET /oauth2callback`: Handle Google OAuth callback.
- `GET /auth_status`: Check Google authorization status.
- `POST /send_email`: Send an email via Gmail.
- `POST /create_event`: Create a Google Calendar event.
- `WS /ws/{session_id}`: WebSocket endpoint for chat.

## Notes

- Make sure your Google Cloud project has Gmail and Calendar APIs enabled.
- The backend is CORS-enabled for easy frontend integration.
- Session memory is stored locally in a SQLite database.

## Development

- All code changes should be made in the backend files listed above.
- Frontend integration is possible via HTTP or WebSocket requests.

## License

MIT License (or specify your license here)
