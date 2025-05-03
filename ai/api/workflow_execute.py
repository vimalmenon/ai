from fastapi import APIRouter

from ai.services import ExecuteWorkflowService

router = APIRouter()


@router.post("/execute/{wf_id}", tags=["execute"])
async def execute_workflow(wf_id: str):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService(wf_id).execute()}
