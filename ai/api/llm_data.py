from fastapi import APIRouter

router = APIRouter()


@router.get("/db", tags=["llm_data"])
async def get_llm_data_from_db():
    pass
