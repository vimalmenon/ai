from langchain_openai import ChatOpenAI

from ai.config import env

openai_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=env.temperature,
)
