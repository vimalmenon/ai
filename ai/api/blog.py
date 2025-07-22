from fastapi import APIRouter

router = APIRouter()


@router.get("/topic", tags=["blog"])
async def get_blog_topic():
    return {"data": []}
