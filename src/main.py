from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.core.config import Config

def create_app() -> FastAPI:
    Config.validate()

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

    app.include_router(router)

    return app

app = create_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=Config.PORT)
