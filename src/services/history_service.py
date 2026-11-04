from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory
from src.core.config import Config
from src.services.interfaces import IHistoryService


class UpstashHistoryService(IHistoryService):
    """
    Concrete implementation of IHistoryService using Upstash Redis.
    
    This service provides persistent conversation history using Upstash Redis.
    """
    
    def get_history(self, session_id: str):
        """
        Retrieve conversation history for a given session from Upstash Redis.
        
        Args:
            session_id: Unique identifier for the conversation session
            
        Returns:
            UpstashRedisChatMessageHistory: A chat message history object
        """
        return UpstashRedisChatMessageHistory(
            url=Config.UPSTASH_REDIS_REST_URL,
            token=Config.UPSTASH_REDIS_REST_TOKEN,
            session_id=session_id,
            ttl=3600
        )
