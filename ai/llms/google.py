from langchain.chat_models import init_chat_model

from ai.config import env

google_llm = init_chat_model(
    model_provider="google", temperature=env.temperature, model="gemini-1.5-pro"
)
