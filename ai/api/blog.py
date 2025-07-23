from fastapi import APIRouter

from ai.services import BlogService

router = APIRouter()


@router.get("/topic", tags=["blog"])
async def get_blog_topic():
    result = BlogService().get_topics()
    return {"data": result}
