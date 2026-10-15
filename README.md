# FastAPI AI Agent

A production-ready AI agent built with **FastAPI** + **LangChain** + **Ollama**.
Supports tool use, per-session memory, streaming responses, and background tasks.

---

## Features

- **AI Agent** with tool calling (web search, calculator, weather, URL summarizer)
- **Per-session memory** — each user gets isolated conversation history
- **Streaming** — Server-Sent Events for real-time token output
- **Background tasks** — fire-and-forget async task execution
- **n8n ready** — webhook endpoint for workflow automation
- **Docker** — one command to run everything
- **Swagger UI** — auto-generated API docs at `/docs`

---

## Project Structure

```
fastapi-ai-agent/
├── app/
│   ├── main.py               # FastAPI app entry point
│   ├── agent/
│   │   ├── agent.py          # AIAgent class with session memory
│   │   └── tools.py          # LangChain tools (search, calc, weather, URL)
│   ├── api/
│   │   └── routes.py         # All API endpoints
│   ├── core/
│   │   ├── config.py         # Pydantic settings
│   │   └── dependencies.py   # DI: agent singleton, session ID, API key
│   └── models/
│       └── schemas.py        # Pydantic request/response models
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-ai-agent.git
cd fastapi-ai-agent
```

### 2. Set up environment

```bash
cp .env.example .env
# Ensure Ollama is running: ollama serve
# Pull your model: ollama pull llama3
```

### 3a. Run locally

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3b. Run with Docker

```bash
docker-compose up --build
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root info |
| `POST` | `/agent/chat` | Chat with memory |
| `POST` | `/agent/chat/stream` | Streaming SSE response |
| `POST` | `/agent/task` | Background task (async) |
| `DELETE` | `/agent/session/{id}` | Clear session memory |
| `GET` | `/agent/sessions` | List active sessions |
| `GET` | `/agent/health` | Health check |

---

## Example Usage

### Chat

```bash
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -H "X-Session-Id: user-123" \
  -d '{"message": "What is 144 divided by 12?"}'
```

**Response:**
```json
{
  "reply": "144 divided by 12 is 12.",
  "session_id": "user-123",
  "tokens_used": 0,
  "tool_calls": [{"tool": "calculator", "output": "12.0"}]
}
```

### Streaming

```bash
curl -X POST http://localhost:8000/agent/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about FastAPI"}' \
  --no-buffer
```

### Background Task

```bash
curl -X POST http://localhost:8000/agent/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Summarize the benefits of n8n automation"}'
```

---

## Available Tools

| Tool | Description |
|------|-------------|
| `search_web` | Web search (plug in Tavily/SerpAPI) |
| `calculator` | Safe math expression evaluator |
| `get_weather` | Weather by city (plug in OpenWeatherMap) |
| `summarize_url` | Fetch and return URL content |

---

## n8n Integration

Point an n8n HTTP Request node to:

```
POST http://localhost:8000/agent/chat
Headers: X-Session-Id: {{$workflow.id}}
Body: {"message": "{{$json.input}}"}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3` | Model to use |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection |
| `MAX_TOKENS` | `1000` | Max response tokens |
| `TEMPERATURE` | `0.7` | Sampling temperature |
| `DEBUG` | `false` | Enable verbose agent logs |

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://langchain.com/)
- [Ollama](https://ollama.ai/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [Docker](https://www.docker.com/)
- [Redis](https://redis.io/)

---

## License

MIT
