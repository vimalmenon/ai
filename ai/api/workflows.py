from fastapi import APIRouter

from ai.model import (
    CreateNodeRequest,
    UpdateWorkflowRequest,
    WorkflowNodeRequest,
    WorkflowSlimModel,
)
from ai.services import ExecuteWorkflowService, WorkflowNodeService, WorkflowService

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


@router.put("/node/{wf_id}", tags=["workflow"])
async def create_workflow_node(wf_id: str, body: CreateNodeRequest):
    """Create the node for workflow"""
    return {"data": WorkflowNodeService().create_workflow_node(wf_id, body)}


@router.post("/node/{wf_id}/{id}", tags=["workflow"])
async def update_workflow_node(wf_id: str, id: str, data: WorkflowNodeRequest):
    """Updated the node for workflow"""
    return {"data": WorkflowNodeService().update_workflow_node(wf_id, id, data)}


@router.delete("/node/{wf_id}/{id}", tags=["workflow"])
async def delete_workflow_node(wf_id: str, id: str):
    """Delete the node for workflow"""
    return {"data": WorkflowNodeService().delete_workflow_nodes(wf_id, id)}


@router.post("/execute/{wf_id}", tags=["workflow"])
async def execute_workflow(wf_id: str):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService(wf_id).execute()}


@router.delete("/{id}", tags=["workflow"])
async def delete_workflows_by_id(id: str):
    """Give the workflow detail by ID"""
    return {"data": WorkflowService().delete_workflows_by_id(id)}


@router.get("/{id}", tags=["workflow"])
async def get_workflows_by_id(id: str):
    """Give the workflow detail by ID"""
    return {"data": WorkflowService().get_workflow_by_id(id)}


@router.get("/history", tags=["workflow"])
async def get_workflow_history():
    """This list out all workflows details"""
    return {"data": []}
