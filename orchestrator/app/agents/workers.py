from functools import lru_cache
from typing import Dict, Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# Import pour Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .tools import real_code_tools, real_doc_tools, real_test_tools, real_diag_tools
from ..config import settings
from ..graph.state import AgentState

WORKER_PROMPT = PromptTemplate.from_template("""
You are a specialized {role} agent in a multi-agent system.

Your role: {role}
Task: {task_description}
Code Context: {code_context}

Use the available tools to complete your specific task.
Be precise and thorough in your analysis.

Question: What should I do to complete this task?
Thought: I need to analyze the task and use appropriate tools.
Action: 
""")

# CORRECTIF CRITIQUE: Implmentation fonctionnelle de la factory.
@lru_cache(maxsize=5)  # CORRECTION IA-1: Augment pour 5 agents (avec Gemini)
def get_agent_executor(agent_type: str) -> AgentExecutor:
    """Cre et configure un AgentExecutor  la demande, puis le met en cache."""
    if agent_type == "code_generation":
        llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=settings.OPENAI_API_KEY)
        tools = real_code_tools
    elif agent_type == "documentation":
        llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.2, api_key=settings.ANTHROPIC_API_KEY)
        tools = real_doc_tools
    elif agent_type == "testing":  # CORRECTION IA-1: Ajout agent testing
        llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=settings.OPENAI_API_KEY)  # GPT-4 pour tests
        tools = real_test_tools
    elif agent_type == "diag_postgresql":
        llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=settings.OPENAI_API_KEY)
        tools = real_diag_tools
    elif agent_type == "gemini_rapid" and GEMINI_AVAILABLE:
        # Agent Gemini pour prototypage rapide et conomique
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=settings.GOOGLE_API_KEY or settings.GEMINI_API_KEY
        )
        tools = real_code_tools  # Utilise les mmes outils que code_generation
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    prompt = WORKER_PROMPT.partial(role=agent_type)
    return AgentExecutor(agent=create_react_agent(llm, tools, prompt), tools=tools, verbose=True, handle_parsing_errors=True)

async def worker_node_wrapper(state: AgentState, agent_key: str) -> Dict[str, Any]:
    """Wrapper asynchrone qui excute la tche pour un agent donn."""
    agent_executor = get_agent_executor(agent_key)
    input_payload = {"task_description": state["task_description"], "code_context": state.get("results", {}).get("code_generation", state.get("code_context", ""))}
    try:
        response = await agent_executor.ainvoke(input_payload)
        state["results"][agent_key] = response["output"]
    except Exception as e:
        state["errors"].append(f"Error in {agent_key}: {e}")
    state["next"] = "supervisor"
    return state 