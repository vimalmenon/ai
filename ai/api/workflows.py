from fastapi import APIRouter

from ai.enum import LLMs
from ai.model import CreateNodeRequest, CreateWorkflowRequest, UpdateWorkflowRequest
from ai.services import WorkflowService
from ai.workflows import TopicWorkflow

router = APIRouter()


@router.get("", tags=["workflow"])
async def get_workflows():
    """This list out all workflows details"""
    return {"data": WorkflowService().get_workflows()}


@router.put("/create", tags=["workflow"])
async def create_workflow(body: CreateWorkflowRequest):
    """Create workflow"""
    return {"data": WorkflowService().create_workflow(body)}


@router.post("/{id}", tags=["workflow"])
async def update_workflow(wf_id: str, body: UpdateWorkflowRequest):
    """Update workflow"""
    return {"data": WorkflowService().update_workflow(wf_id)}


@router.put("/node/{wf_id}", tags=["workflow"])
async def create_workflow_node(wf_id: str, body: CreateNodeRequest):
    """Create the node for workflow"""
    return {"data": WorkflowService().create_workflow_node(wf_id, body)}


@router.post("/node/{wf_id}/{id}", tags=["workflow"])
async def update_workflow_node(wf_id: str, id: str):
    """Updated the node for workflow"""
    return {"data": WorkflowService().update_workflow_node(id)}


@router.delete("/node/{wf_id}/{id}", tags=["workflow"])
async def delete_workflow_node(wf_id: str, id: str):
    """Delete the node for workflow"""
    return {"data": WorkflowService().delete_workflow_nodes(wf_id, id)}


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
