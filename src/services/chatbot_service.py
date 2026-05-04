from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.config import Config
from src.services.history_service import HistoryService

class ChatbotService:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.7
        )
        self.system_prompt = Config.SYSTEM_PROMPT

    def get_response(self, user_message: str, session_id: str):
        history = HistoryService.get_history(session_id)
        
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
