from fastapi import APIRouter

from ai.services import DbService

router = APIRouter()


@router.get("/db", tags=["llm_data"])
async def get_llm_data_from_db():
    data = DbService().get_by_id()
    return {"data": data}
