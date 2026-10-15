from pydantic import BaseModel, Field
from typing import Any
from enum import Enum


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None
    stream: bool = False


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tokens_used: int
    tool_calls: list[dict[str, Any]] = []


class AgentTask(BaseModel):
    task: str = Field(..., description="Task for the agent to execute")
    context: dict[str, Any] = {}


class TaskResponse(BaseModel):
    result: str
    steps: list[str]
    status: str
