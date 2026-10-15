from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="FastAPI AI Agent",
    description=(
        "Production-ready AI agent with tool use, per-session memory, "
        "streaming, and background task support. "
        "Built with FastAPI + LangChain + Ollama."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/agent/health",
        "endpoints": {
            "chat": "POST /agent/chat",
            "stream": "POST /agent/chat/stream",
            "task": "POST /agent/task",
            "clear_session": "DELETE /agent/session/{id}",
        },
    }
