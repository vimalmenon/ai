from fastapi import APIRouter

from ai.model import CreateExecuteWorkflowRequest
from ai.services import ExecuteWorkflowService

router = APIRouter()


@router.put("/{wf_id}", tags=["Execute"])
async def execute_workflow(wf_id: str, data: CreateExecuteWorkflowRequest):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService(wf_id).execute()}


@router.post("/resume/{wf_id}", tags=["Execute"])
async def resume_workflow(wf_id: str):
    """This will resume the workflow"""
    return {"data": ExecuteWorkflowService(wf_id).resume_execute()}


@router.get("/{wf_id}", tags=["Execute"])
async def get_workflow(wf_id: str):
    """This will get the workflow"""
    return {"data": []}
