from fastapi import APIRouter

from ai.model import LLMResponse
from ai.services import ListLLMServices
from ai.utilities import generate_uuid

router = APIRouter()


@router.get("/uuid/")
async def get_uuid():
    """This List out all llm's"""
    return {"data": generate_uuid()}


@router.get("/llm", response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {"data": ListLLMServices().list_llm_details()}
