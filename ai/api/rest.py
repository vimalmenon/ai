from fastapi import APIRouter

from ai.model import LLMResponse
from ai.services import ListLLMServices, ToolService
from ai.utilities import generate_uuid

router = APIRouter()


@router.get("/uuid")
async def get_uuid():
    """This List out all llm's"""
    return {"data": generate_uuid()}


@router.get("/llms", response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {"data": ListLLMServices().list_llm_details()}


@router.get("/tools")
async def get_tools():
    """This List out all available tools"""
    return {"data": ToolService().get_tools()}
