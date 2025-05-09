from langchain_deepseek import ChatDeepSeek

from ai.config import env

deepseek_llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=env.temperature,
    max_tokens=None,
)
