from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from ai.llms.ollama import ollama_llm
from ai.tools import tools

checkpointer = MemorySaver()

agent_executor = create_react_agent(
    ollama_llm, tools, checkpointer=checkpointer, name="Elara"
)
