from functools import lru_cache
from typing import Dict, Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from orchestrator.app.agents.tools import real_code_tools, real_doc_tools, real_test_tools
from orchestrator.app.config import settings
from orchestrator.app.graph.state import AgentState

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

# CORRECTIF CRITIQUE: Implémentation fonctionnelle de la factory.
@lru_cache(maxsize=3)  # CORRECTION IA-1: Augmenté pour 3 agents
def get_agent_executor(agent_type: str) -> AgentExecutor:
    """Crée et configure un AgentExecutor à la demande, puis le met en cache."""
    if agent_type == "code_generation":
        llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=settings.OPENAI_API_KEY)
        tools = real_code_tools
    elif agent_type == "documentation":
        llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.2, api_key=settings.ANTHROPIC_API_KEY)
        tools = real_doc_tools
    elif agent_type == "testing":  # CORRECTION IA-1: Ajout agent testing
        llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=settings.OPENAI_API_KEY)  # GPT-4 pour tests
        tools = real_test_tools
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    prompt = WORKER_PROMPT.partial(role=agent_type)
    return AgentExecutor(agent=create_react_agent(llm, tools, prompt), tools=tools, verbose=True, handle_parsing_errors=True)

async def worker_node_wrapper(state: AgentState, agent_key: str) -> Dict[str, Any]:
    """Wrapper asynchrone qui exécute la tâche pour un agent donné."""
    agent_executor = get_agent_executor(agent_key)
    input_payload = {"task_description": state["task_description"], "code_context": state.get("results", {}).get("code_generation", state.get("code_context", ""))}
    try:
        response = await agent_executor.ainvoke(input_payload)
        state["results"][agent_key] = response["output"]
    except Exception as e:
        state["errors"].append(f"Error in {agent_key}: {e}")
    state["next"] = "supervisor"
    return state 