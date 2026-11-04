from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as chat_router
from src.core.config import Config
from src.core.container import container
from src.services.interfaces import IChatbotService, IHistoryService, ISearchService
from src.services.history_service import UpstashHistoryService
from src.services.chatbot_service import GeminiChatbotService
from src.services.search_service import TinyFishSearchService


def register_services():
    """
    Register all services with the dependency injection container.
    
    This function registers concrete implementations for all service interfaces,
    enabling the container to provide instances when requested.
    """
    # Register history service
    container.register(IHistoryService, UpstashHistoryService)
    
    # Register search service (TinyFish) - only if API key is configured
    if Config.TINYFISH_API_KEY:
        container.register(ISearchService, TinyFishSearchService)
    
    # Register chatbot service with its dependencies
    history_service = container.get(IHistoryService)
    search_service = None
    if Config.SEARCH_ENABLED and Config.TINYFISH_API_KEY:
        try:
            search_service = container.get(ISearchService)
        except:
            pass
    container.register_instance(IChatbotService, GeminiChatbotService(history_service, search_service))


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This function:
    1. Validates configuration
    2. Registers services with the DI container
    3. Creates the FastAPI app
    4. Configures middleware
    5. Includes routers
    
    Returns:
        Configured FastAPI application instance
    """
    Config.validate()
    register_services()

    app = FastAPI(
        title="Gemini Chatbot API",
        description="A memory-augmented chatbot using Google Gemini and Upstash Redis",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router)

    return app

app = create_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=Config.PORT)
