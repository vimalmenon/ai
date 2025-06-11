from fastapi import APIRouter

from ai.model import (
    CreateNodeRequest,
    WorkflowNodeRequest,
)
from ai.services import WorkflowNodeService, WorkflowService

router = APIRouter()


@router.put("/{wf_id}", tags=["node"])
async def create_workflow_node(wf_id: str, body: CreateNodeRequest):
    """Create the node for workflow"""
    WorkflowNodeService().create_workflow_node(wf_id, body)
    return {"data": WorkflowService().get_workflow_by_id(wf_id)}


@router.post("/{wf_id}/{id}", tags=["node"])
async def update_workflow_node(wf_id: str, id: str, data: WorkflowNodeRequest):
    """Updated the node for workflow"""
    WorkflowNodeService().update_workflow_node(wf_id, id, data)
    return {"data": WorkflowService().get_workflow_by_id(wf_id)}


@router.delete("/{wf_id}/{id}", tags=["node"])
async def delete_workflow_node(wf_id: str, id: str):
    """Delete the node for workflow"""
    WorkflowNodeService().delete_workflow_nodes(wf_id, id)
    return {"data": WorkflowService().get_workflow_by_id(wf_id)}
