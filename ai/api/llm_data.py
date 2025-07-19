from fastapi import APIRouter

from ai.services import DbService

router = APIRouter()


@router.get("/db/{wf_id}", tags=["llm_data"])
async def get_llm_data_from_db(wf_id: str):
    data = DbService().get_by_id(wf_id)
    return {"data": data}
