from langchain.chat_models import init_chat_model

from ai.config import env

ollama_llm = init_chat_model(
    "mistral", model_provider="ollama", temperature=env.temperature
)
