from fastapi import APIRouter

from ai.model import CreateExecuteWorkflowRequest
from ai.services import ExecuteWorkflowService

router = APIRouter()


@router.post("/{wf_id}", tags=["Execute"])
async def execute_workflow(wf_id: str, data: CreateExecuteWorkflowRequest):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService(wf_id).execute()}
