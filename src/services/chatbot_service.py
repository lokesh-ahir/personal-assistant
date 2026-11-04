from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.config import Config
from src.services.interfaces import IChatbotService, IHistoryService


class GeminiChatbotService(IChatbotService):
    """
    Concrete implementation of IChatbotService using Google Gemini.
    
    This service uses Google Gemini LLM to generate responses,
    with conversation history retrieved from a history service.
    """
    
    def __init__(self, history_service: IHistoryService = None):
        """
        Initialize the chatbot service.
        
        Args:
            history_service: An instance of IHistoryService for retrieving conversation history.
                           If None, it will be injected via the container.
        """
        self.model = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.7
        )
        self.system_prompt = Config.SYSTEM_PROMPT
        self.history_service = history_service
    
    def get_response(self, user_message: str, session_id: str) -> str:
        """
        Get a response from the chatbot for a user message.
        
        Args:
            user_message: The message from the user
            session_id: Unique identifier for the conversation session
            
        Returns:
            The chatbot's response as a string
        """
        history = self.history_service.get_history(session_id)
        
        messages = [SystemMessage(content=self.system_prompt)]
        messages.extend(history.messages)
        messages.append(HumanMessage(content=user_message))

        response = self.model.invoke(messages)

        content = response.content
        if isinstance(content, list):
            content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
        
        history.add_user_message(user_message)
        history.add_ai_message(content)

        return content
