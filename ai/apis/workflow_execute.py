from fastapi import APIRouter

from ai.model import CreateExecuteWorkflowRequest, ResumeWorkflowRequest
from ai.services import ExecuteWorkflowService

router = APIRouter()


@router.put("/{wf_id}", tags=["Execute"])
async def create_executed_workflow(wf_id: str, data: CreateExecuteWorkflowRequest):
    """This will execute the workflow"""
    return {"data": ExecuteWorkflowService().create_executed_workflow(wf_id, data)}


@router.post("/resume/{wf_id}/{exec_id}", tags=["Execute"])
async def resume_workflow(wf_id: str, exec_id: str, data: ResumeWorkflowRequest):
    """This will resume the pending workflow"""
    return {"data": ExecuteWorkflowService().resume_execute(wf_id, exec_id, data)}


@router.get("/{wf_id}", tags=["Execute"])
async def get_workflow(wf_id: str):
    """This will get the executed workflow"""
    return {"data": ExecuteWorkflowService().get(wf_id)}


@router.get("/{wf_id}/{exec_id}", tags=["Execute"])
async def get_executed_workflow(wf_id: str, exec_id: str):
    """This will get the executed workflow"""
    return {"data": ExecuteWorkflowService().get_executed_workflow_id(wf_id, exec_id)}


@router.delete("/{wf_id}/{exec_id}", tags=["Execute"], status_code=204)
async def delete_workflow(wf_id: str, exec_id: str):
    """This will delete the executed workflow"""
    ExecuteWorkflowService().delete(wf_id, exec_id)
