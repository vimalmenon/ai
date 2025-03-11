from uuid import uuid4

from fastapi import APIRouter

from ai.model import LLMResponse
from ai.services import ListLLMServices

router = APIRouter()


@router.get("/uuid/")
async def get_uuid():
    """This List out all llm's"""
    return {"data": uuid4()}


@router.get("/llm", response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {"data": ListLLMServices().list_llm_details()}
