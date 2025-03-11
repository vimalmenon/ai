from uuid import uuid4

from fastapi import APIRouter

from ai.config import env
from ai.enum import LLMs
from ai.model import LLMResponse

router = APIRouter()


@router.get("/uuid/")
async def get_uuid():
    """This List out all llm's"""
    return {"data": uuid4()}


@router.get("/llm", response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {
        "data": [
            {
                "name": LLMs.DEEPSEEK,
                "model": "deepseek-chat",
                "supported": LLMs.DEEPSEEK.value in env.supported_llm,
            },
            {
                "name": LLMs.GOOGLE,
                "model": "gemini-1.5-pro",
                "supported": LLMs.GOOGLE.value in env.supported_llm,
            },
            {
                "name": LLMs.OLLAMA,
                "model": "mistral",
                "supported": LLMs.OLLAMA.value in env.supported_llm,
            },
        ]
    }
