from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["ai messages"])
async def get_ai_messages():
    return {"data": []}
