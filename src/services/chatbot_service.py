from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.config import Config
from src.services.interfaces import IChatbotService, IHistoryService, ISearchService
from src.core.container import container


class GeminiChatbotService(IChatbotService):
    """
    Concrete implementation of IChatbotService using Google Gemini.
    
    This service uses Google Gemini LLM to generate responses,
    with conversation history retrieved from a history service.
    Optionally uses search service for web search capability.
    """
    
    def __init__(self, history_service: IHistoryService = None, search_service: ISearchService = None):
        """
        Initialize the chatbot service.
        
        Args:
            history_service: An instance of IHistoryService for retrieving conversation history.
            search_service: An instance of ISearchService for web search capability.
                           If None, web search will not be available.
        """
        self.model = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.7
        )
        self.system_prompt = Config.SYSTEM_PROMPT
        self.history_service = history_service
        self.search_service = search_service
        self.search_enabled = Config.SEARCH_ENABLED and search_service is not None
    
    def _should_search(self, user_message: str) -> bool:
        """
        Determine if the user's message requires web search.
        
        Args:
            user_message: The message from the user
            
        Returns:
            True if web search should be performed, False otherwise
        """
        if not self.search_enabled:
            return False
        
        # Simple heuristic: if the message contains question words or seems like a factual query
        # This can be enhanced with more sophisticated logic
        question_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'can you', 'could you']
        user_message_lower = user_message.lower().strip()
        
        # Check if it's a question
        if any(user_message_lower.startswith(word) for word in question_words):
            return True
        
        # Check if it ends with a question mark
        if user_message_lower.endswith('?'):
            return True
        
        # Check for search-related keywords
        search_keywords = ['search', 'find', 'look up', 'what is', 'who is', 'latest', 'news', 'information']
        if any(keyword in user_message_lower for keyword in search_keywords):
            return True
        
        return False
    
    def get_response(self, user_message: str, session_id: str) -> str:
        """
        Get a response from the chatbot for a user message.
        
        If web search is enabled and the message requires it, the chatbot will
        search the web and include the results in the context before generating
        a response.
        
        Args:
            user_message: The message from the user
            session_id: Unique identifier for the conversation session
            
        Returns:
            The chatbot's response as a string
        """
        history = self.history_service.get_history(session_id)
        
        messages = [SystemMessage(content=self.system_prompt)]
        messages.extend(history.messages)
        
        # Check if we should perform a web search
        if self._should_search(user_message):
            try:
                search_results = self.search_service.search(
                    query=user_message,
                    limit=3  # Get top 3 results
                )
                
                # Format search results for the LLM
                search_context = "\n\n-- Web Search Results --\n"
                for idx, result in enumerate(search_results.results, 1):
                    search_context += f"{idx}. {result.title}\n"
                    search_context += f"   URL: {result.url}\n"
                    if result.snippet:
                        search_context += f"   Snippet: {result.snippet}\n"
                    search_context += "\n"
                
                # Add search results as a system message
                messages.append(SystemMessage(content=search_context))
                
            except Exception as e:
                # If search fails, continue without it
                # Could log this error in production
                pass
        
        messages.append(HumanMessage(content=user_message))

        response = self.model.invoke(messages)

        content = response.content
        if isinstance(content, list):
            content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
        
        history.add_user_message(user_message)
        history.add_ai_message(content)

        return content
