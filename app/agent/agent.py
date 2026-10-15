from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from app.agent.tools import TOOLS
from app.core.config import get_settings

settings = get_settings()

PROMPT_TEMPLATE = """You are a helpful AI assistant with access to tools.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to be concise and accurate. If you are unsure about something, say so.

Question: {input}
Thought: {agent_scratchpad}"""


def build_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(PROMPT_TEMPLATE)


def create_agent() -> AgentExecutor:
    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.temperature,
        num_predict=settings.max_tokens,
    )
    prompt = build_prompt()
    agent = create_react_agent(llm, TOOLS, prompt)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=settings.debug,
        max_iterations=5,
        handle_parsing_errors=True,
    )


class AIAgent:
    """Stateful AI agent with per-session conversation memory."""

    def __init__(self):
        self.sessions: dict[str, AgentExecutor] = {}

    def get_session(self, session_id: str) -> AgentExecutor:
        if session_id not in self.sessions:
            memory = ConversationBufferWindowMemory(
                memory_key="chat_history",
                return_messages=True,
                k=10,
            )
            llm = ChatOllama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=settings.temperature,
                num_predict=settings.max_tokens,
            )
            prompt = build_prompt()
            agent = create_react_agent(llm, TOOLS, prompt)
            self.sessions[session_id] = AgentExecutor(
                agent=agent,
                tools=TOOLS,
                memory=memory,
                verbose=settings.debug,
                max_iterations=5,
                handle_parsing_errors=True,
            )
        return self.sessions[session_id]

    async def run(self, message: str, session_id: str) -> dict:
        executor = self.get_session(session_id)
        result = await executor.ainvoke({"input": message})
        return {
            "reply": result["output"],
            "tool_calls": result.get("intermediate_steps", []),
        }

    def clear_session(self, session_id: str):
        self.sessions.pop(session_id, None)

    def list_sessions(self) -> list[str]:
        return list(self.sessions.keys())