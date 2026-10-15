from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "FastAPI AI Agent"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    redis_url: str = "redis://localhost:6379"
    max_tokens: int = 1000
    temperature: float = 0.7
    debug: bool = False

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
