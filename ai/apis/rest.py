from fastapi import APIRouter

from ai.config import Env
from ai.model import AppInfo, LLMResponse
from ai.model.enums import Service, StructuredOutputType, Tool, WorkflowType
from ai.services import LlmService
from ai.utilities import generate_uuid

router = APIRouter()


@router.get("/uuid")
async def get_uuid():
    """This List out all llm's"""
    return {"data": generate_uuid()}


@router.get("/llms", response_model=LLMResponse)
async def get_llm():
    """This List out all llm's"""
    return {"data": LlmService().list_llm_details()}


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


@router.get("/structured_output_types")
async def get_structured_output_types():
    """This List out all available structured output types"""
    return {"data": list(StructuredOutputType)}


@router.get("/health")
async def get_health():
    return {"data": []}


@router.get("/info")
async def get_info():
    """This List out all available info"""
    env = Env()
    return {"data": AppInfo(env=env.env, version=env.version)}
