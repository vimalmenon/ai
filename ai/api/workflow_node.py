from fastapi import APIRouter

from ai.model import (
    CreateNodeRequest,
    WorkflowNodeRequest,
)
from ai.services import WorkflowNodeService

router = APIRouter()


@router.put("/node/{wf_id}", tags=["node"])
async def create_workflow_node(wf_id: str, body: CreateNodeRequest):
    """Create the node for workflow"""
    return {"data": WorkflowNodeService().create_workflow_node(wf_id, body)}


@router.post("/node/{wf_id}/{id}", tags=["node"])
async def update_workflow_node(wf_id: str, id: str, data: WorkflowNodeRequest):
    """Updated the node for workflow"""
    return {"data": WorkflowNodeService().update_workflow_node(wf_id, id, data)}


@router.delete("/node/{wf_id}/{id}", tags=["node"])
async def delete_workflow_node(wf_id: str, id: str):
    """Delete the node for workflow"""
    return {"data": WorkflowNodeService().delete_workflow_nodes(wf_id, id)}
