# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run with Docker
docker-compose up --build
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file.py -v
```

### Ollama Setup
```bash
# Start Ollama server
ollama serve

# Pull a model
ollama pull llama3
```

## Architecture

This is a FastAPI-based AI agent using LangChain with Ollama.

### Core Flow
1. **Request** → `routes.py` endpoint → `AIAgent.run()`
2. **Session Management** → `AIAgent.get_session()` creates/retrieves per-session `AgentExecutor` with memory
3. **Tool Execution** → LangChain agent calls tools from `tools.py` as needed

### Key Components

- **`app/agent/agent.py`** — `AIAgent` class manages per-session `AgentExecutor` instances. Each session gets its own memory (`ConversationBufferWindowMemory`, k=10). Uses `ChatOllama` with `create_tool_calling_agent`.

- **`app/agent/tools.py`** — LangChain `@tool` decorated functions. Currently stubbed implementations for `search_web`, `get_weather`. `calculator` uses `eval()` with character whitelist. `summarize_url` fetches URL content via httpx.

- **`app/core/dependencies.py`** — FastAPI dependency injection. `get_agent()` returns a singleton `AIAgent`. `get_session_id()` extracts session ID from `X-Session-Id` header or generates UUID.

- **`app/api/routes.py`** — All endpoints under `/agent` prefix. Chat uses session memory; streaming bypasses the agent entirely (direct LLM stream); background tasks queue via FastAPI's `BackgroundTasks`.

### Tool Integration

To add a new tool:
1. Create a `@tool` decorated function in `app/agent/tools.py`
2. Add it to the `TOOLS` list at the bottom of the file

### Environment

Config via `.env` — see `.env.example`. Uses `OLLAMA_BASE_URL` and `OLLAMA_MODEL`. Settings loaded via `pydantic-settings` in `app/core/config.py`.