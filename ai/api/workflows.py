from fastapi import APIRouter

from ai.enum import LLMs
from ai.model import CreateWorkflowRequest
from ai.services import WorkflowService
from ai.workflows import TopicWorkflow

router = APIRouter()


@router.get("", tags=["workflow"])
async def get_workflows():
    """This list out all workflows details"""
    return {"data": WorkflowService().get_workflows()}


@router.put("/create", tags=["workflow"])
async def create_workflow(body: CreateWorkflowRequest):
    """Create workflow to execute"""
    return {"data": WorkflowService().create_workflow(body)}


@router.post("/execute_workflow/{llm}", tags=["workflow"])
async def execute_workflow(llm: LLMs):
    """This will execute the workflow"""
    return TopicWorkflow(llm).execute()


@router.delete("/{id}", tags=["workflow"])
async def delete_workflows_by_id(id: str):
    """Give the workflow detail by ID"""
    return {"data": WorkflowService().delete_workflows_by_id(id)}


@router.get("/{id}", tags=["workflow"])
async def get_workflows_by_id(id: str):
    """Give the workflow detail by ID"""
    return {"data": WorkflowService().get_workflow_by_id(id)}
