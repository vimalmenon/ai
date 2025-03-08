from fastapi import APIRouter

from ai.services import WorkflowService

router = APIRouter()


@router.get("/", tags=["workflow"])
async def get_workflows():
    """This List out all workflows details"""
    return WorkflowService().get_workflows()
