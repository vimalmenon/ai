from fastapi import APIRouter

from ai.services import DbService

router = APIRouter()


@router.get("/db", tags=["llm_data"])
async def get_llm_data_from_db():
    data = DbService().get_by_id()
    return {"data": data}


@router.delete("/db/{id}", tags=["llm_data"])
async def delete_llm_data_from_db(id: str):
    """Delete LLM data by ID"""
    DbService().delete_by_id(id)
    return {"message": "LLM data deleted successfully"}
