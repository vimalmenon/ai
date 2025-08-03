from fastapi import APIRouter

from ai.services import AiMessageService

router = APIRouter()


@router.get("/{id}", tags=["ai messages"])
async def get_ai_messages(id: str):
    messages = AiMessageService().get_messages(id)
    return {"data": messages}
