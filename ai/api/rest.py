from fastapi import APIRouter

from ai.model import LLMResponse, WorkflowType
from ai.model.others import Service, Tool
from ai.services import DbService, ListLLMServices
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


@router.get("/from_db/{id}")
async def get_from_db(id: str):
    """Get from db"""
    data = DbService().get_by_id(id)
    return {"data": data}
