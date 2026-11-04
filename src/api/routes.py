from fastapi import APIRouter, HTTPException, Depends
from src.api.schemas import ChatRequest, ChatResponse
from src.services.interfaces import IChatbotService
from src.core.container import container

router = APIRouter()


def get_chatbot_service() -> IChatbotService:
    """
    Dependency injection for chatbot service.
    
    Returns:
        An instance of IChatbotService from the container
    """
    return container.get(IChatbotService)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chatbot_service: IChatbotService = Depends(get_chatbot_service)
):
    """
    Endpoint for chat interaction.
    
    This endpoint accepts a user message and optional session_id,
    and returns a chatbot response with context from previous messages.
    
    Args:
        request: ChatRequest containing message and session_id
        chatbot_service: Injected chatbot service instance
        
    Returns:
        ChatResponse with the chatbot's response and session_id
        
    Raises:
        HTTPException: If message is empty or an error occurs
    """
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
    """
    Health check endpoint.
    
    Returns:
        A simple status message indicating the service is healthy
    """
    return {"status": "healthy"}
