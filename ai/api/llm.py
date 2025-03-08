from fastapi import APIRouter

from ai.model import LLMResponse

router = APIRouter()


@router.get("/", tags=["llm"], response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {
        "data": [
            {"name": "Deepseek", "model": "deepseek-chat"},
            {"name": "Google", "model": "gemini-1.5-pro"},
        ]
    }
