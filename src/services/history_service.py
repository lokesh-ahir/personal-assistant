from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory
from src.core.config import Config

class HistoryService:
    @staticmethod
    def get_history(session_id: str):
        return UpstashRedisChatMessageHistory(
            url=Config.UPSTASH_REDIS_REST_URL,
            token=Config.UPSTASH_REDIS_REST_TOKEN,
            session_id=session_id,
            ttl=3600
        )
