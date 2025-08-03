from fastapi import APIRouter

from ai.services import AiMessage

router = APIRouter()


@router.get("/{id}", tags=["ai messages"])
async def get_ai_messages(id: str):
    messages = AiMessage().get_messages(id)
    return {"data": messages}
