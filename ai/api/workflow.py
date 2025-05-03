from fastapi import APIRouter

from ai.model import (
    UpdateWorkflowRequest,
    WorkflowSlimModel,
)
from ai.services import ExecuteWorkflowService, WorkflowService

router = APIRouter()


@router.get("", tags=["workflow"])
async def get_workflows():
    """This list out all workflows details"""
    return {"data": WorkflowService().get_workflows()}


@router.put("/create", tags=["workflow"])
async def create_workflow(body: WorkflowSlimModel):
    """Create workflow"""
    return {"data": WorkflowService().create_workflow(body)}


@router.post("/{id}", tags=["workflow"])
async def update_workflow(id: str, body: UpdateWorkflowRequest):
    """Update workflow"""
    return {"data": WorkflowService().update_workflow(id, body)}


@router.delete("/{id}", tags=["workflow"])
async def delete_workflows_by_id(id: str):
    """Give the workflow detail by ID"""
    return {"data": WorkflowService().delete_workflows_by_id(id)}


@router.post("/execute/{wf_id}", tags=["execute"])
async def execute_workflow(wf_id: str):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService(wf_id).execute()}


@router.get("/history", tags=["history"])
async def get_workflow_history():
    """This list out all workflows details"""
    return {"data": []}


@router.get("/{id}", tags=["workflow"])
async def get_workflows_by_id(id: str):
    """Give the workflow detail by ID"""
    return {"data": WorkflowService().get_workflow_by_id(id)}
