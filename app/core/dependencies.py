from fastapi import Depends, Header
from app.agent.agent import AIAgent
from app.core.config import Settings, get_settings
import uuid

_agent_instance: AIAgent | None = None


def get_agent() -> AIAgent:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = AIAgent()
    return _agent_instance


def get_session_id(
    x_session_id: str | None = Header(default=None),
) -> str:
    return x_session_id or str(uuid.uuid4())


def verify_api_key(
    x_api_key: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
):
    # Uncomment to protect endpoints:
    # if x_api_key != settings.internal_api_key:
    #     raise HTTPException(403, "Invalid API key")
    return x_api_key
