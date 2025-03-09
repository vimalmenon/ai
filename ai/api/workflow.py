from fastapi import APIRouter

from ai.enum import LLMs
from ai.services import WorkflowService
from ai.workflows import TopicWorkflow

router = APIRouter()


@router.get("/", tags=["workflow"])
async def get_workflows():
    """This List out all workflows details"""
    return WorkflowService().get_workflows()


@router.post("/execute_workflow/{llm}", tags=["workflow"])
async def execute_workflow(llm: LLMs):
    """This will execute the workflow"""
    return TopicWorkflow(llm).execute()
