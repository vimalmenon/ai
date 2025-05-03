from fastapi import APIRouter

router = APIRouter()


@router.get("/history", tags=["history"])
async def get_workflow_history():
    """This list out all workflows details"""
    return {"data": []}
