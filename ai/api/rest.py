from uuid import uuid4

from fastapi import APIRouter

router = APIRouter()


@router.get("/uuid/")
async def get_uuid():
    """This List out all llm's"""
    return {"data": uuid4()}
