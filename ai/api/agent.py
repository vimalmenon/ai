from fastapi import APIRouter

from ai.services import AgentService

router = APIRouter()


@router.get("/{wf}", tags=["agent"])
async def get_workflows(wf: str):
    """This List out all workflows details"""
    return {"data": AgentService().list_agent_for_workflow()}
