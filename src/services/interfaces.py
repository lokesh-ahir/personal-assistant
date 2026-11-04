from abc import ABC, abstractmethod
from typing import List, Optional


class ISearchService(ABC):
    """Interface for search services."""

    @abstractmethod
    def search(self, query: str, limit: int = 10, **kwargs) -> dict:
        """
        Perform a web search.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return
            **kwargs: Additional search parameters
            
        Returns:
            A dictionary containing search results
        """
        pass


class IHistoryService(ABC):
    """Interface for conversation history services."""

    @abstractmethod
    def get_history(self, session_id: str):
        """
        Retrieve conversation history for a given session.
        
        Args:
            session_id: Unique identifier for the conversation session
            
        Returns:
            A chat message history object that can store and retrieve messages
        """
        pass


class IChatbotService(ABC):
    """Interface for chatbot services."""

    @abstractmethod
    def get_response(self, user_message: str, session_id: str) -> str:
        """
        Get a response from the chatbot for a user message.
        
        Args:
            user_message: The message from the user
            session_id: Unique identifier for the conversation session
            
        Returns:
            The chatbot's response as a string
        """
        pass
