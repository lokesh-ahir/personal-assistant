from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message is required")

        response_text = chatbot_service.get_response(request.message, request.session_id)
        
        return ChatResponse(
            response=response_text,
            session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "healthy"}
