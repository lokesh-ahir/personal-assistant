# Industry Standard Gemini Chatbot (LangChain + Upstash Redis)

A robust, session-based chatbot backend using LangChain, Google Gemini, and Upstash Redis for persistent conversation history.

## 📁 Project Structure

```
gemini_chatbot/
├── src/
│   ├── api/         # FastAPI routes and schemas
│   ├── core/        # Configuration and validation
│   ├── services/    # Business logic (Gemini and Redis History)
│   └── main.py      # FastAPI entry point
├── .env.example     # Env template
├── requirements.txt # Dependencies
└── README.md
```

## ✨ Features

- **Gemini 1.5 Flash**: Fast and intelligent responses.
- **Upstash Redis History**: Remembers context across messages using session IDs.
- **Industry Standard Layout**: Modular, service-oriented architecture.
- **SOLID Principles**: Clear separation of concerns.

## 🚀 Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configuration**:
- Copy `.env.example` to `.env`.
- Add your `GOOGLE_API_KEY`, `UPSTASH_REDIS_REST_URL`, and `UPSTASH_REDIS_REST_TOKEN`.

3. **Run the Server**:
```bash
uvicorn src.main:app --reload --port 5000
```

## 📡 API Endpoints

### Chat (with History)
- **URL**: `/chat`
- **Method**: `POST`
- **Body**:
```json
{
  "message": "My name is John",
  "session_id": "user-123" // Optional: used to track history
}
```
- **Next message**:
```json
{
  "message": "What is my name?",
  "session_id": "user-123"
}
```
- **Response**: "Your name is John."

### Health Check
- **URL**: `/health`
- **Method**: `GET`
