from fastapi import APIRouter

from ai.model import CreateExecuteWorkflowRequest
from ai.services import ExecuteWorkflowService

router = APIRouter()


@router.put("/{wf_id}", tags=["Execute"])
async def execute_workflow(wf_id: str, data: CreateExecuteWorkflowRequest):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService().execute(wf_id, data)}


@router.post("/resume/{wf_id}/{id}", tags=["Execute"])
async def resume_workflow(wf_id: str, id: str):
    """This will resume the pending workflow"""
    return {"data": ExecuteWorkflowService().resume_execute(wf_id, id)}


@router.get("/{wf_id}", tags=["Execute"])
async def get_workflow(wf_id: str):
    """This will get the executed workflow"""
    return {"data": ExecuteWorkflowService().get(wf_id)}


@router.delete("/{wf_id}/{id}", tags=["Execute"])
async def delete_workflow(wf_id: str, id: str):
    """This will delete the executed workflow"""
    return {"data": ExecuteWorkflowService().delete(wf_id, id)}
