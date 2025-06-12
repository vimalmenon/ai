from fastapi import APIRouter

from ai.model import LLMResponse, WorkflowType
from ai.model.others import Service, Tool
from ai.services import ListLLMServices
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
    return {"data": list(Tool)}


@router.get("/services")
async def get_services():
    """This List out all available services"""
    return {"data": list(Service)}


@router.get("/workflow_types")
async def get_workflow_types():
    """This List out all available tools"""
    return {"data": list(WorkflowType)}
