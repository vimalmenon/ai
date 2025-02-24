from langchain_google_genai import ChatGoogleGenerativeAI

from ai.config import env

google_llm = ChatGoogleGenerativeAI(temperature=env.temperature, model="gemini-1.5-pro")
