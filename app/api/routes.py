from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    ChatRequest, ChatResponse,
    AgentTask,
)
from app.core.dependencies import get_agent, get_session_id
from app.agent.agent import AIAgent
import uuid
import json

router = APIRouter(prefix="/agent", tags=["AI Agent"])


# ── Chat (with memory) ───────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session_id: str = Depends(get_session_id),
    agent: AIAgent = Depends(get_agent),
):
    """Send a message to the AI agent. Maintains conversation history per session."""
    try:
        result = await agent.run(
            message=request.message,
            session_id=session_id,
        )
        tool_calls = [
            {"tool": step[0].tool, "output": str(step[1])}
            for step in result["tool_calls"]
            if hasattr(step[0], "tool")
        ]
        return ChatResponse(
            reply=result["reply"],
            session_id=session_id,
            tokens_used=0,
            tool_calls=tool_calls,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Streaming chat (SSE) ─────────────────────────────────
@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    session_id: str = Depends(get_session_id),
):
    """Stream tokens back via Server-Sent Events."""
    from langchain_community.chat_models import ChatOllama
    from app.core.config import get_settings
    settings = get_settings()

    async def token_generator():
        llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.temperature,
        )
        async for chunk in llm.astream(request.message):
            yield f"data: {json.dumps({'token': chunk.content})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={"X-Session-Id": session_id},
    )


# ── Background task ──────────────────────────────────────
@router.post("/task")
async def run_task(
    task: AgentTask,
    background_tasks: BackgroundTasks,
    agent: AIAgent = Depends(get_agent),
):
    """Queue a task to run in the background. Returns immediately."""
    task_id = str(uuid.uuid4())
    session = f"task-{task_id}"

    async def execute():
        result = await agent.run(task.task, session_id=session)
        print(f"[Task {task_id}] {result['reply'][:120]}")

    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "queued"}


# ── Session management ───────────────────────────────────
@router.delete("/session/{session_id}")
async def clear_session(
    session_id: str,
    agent: AIAgent = Depends(get_agent),
):
    """Clear conversation memory for a session."""
    agent.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}


@router.get("/sessions")
async def list_sessions(agent: AIAgent = Depends(get_agent)):
    """List all active session IDs."""
    return {"sessions": agent.list_sessions()}


# ── Health ───────────────────────────────────────────────
@router.get("/health")
async def health():
    return {"status": "ok", "agent": "ready"}
