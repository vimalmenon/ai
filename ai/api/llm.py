from fastapi import APIRouter

from ai.enum import LLMs
from ai.model import LLMResponse

router = APIRouter()


@router.get("/", tags=["llm"], response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {
        "data": [
            {"name": LLMs.DEEPSEEK, "model": "deepseek-chat"},
            {"name": LLMs.GOOGLE, "model": "gemini-1.5-pro"},
            {"name": LLMs.OLLAMA, "model": "mistral"},
        ]
    }
