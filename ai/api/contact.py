from fastapi import APIRouter

router = APIRouter()


@router.post("/", tags=["users"])
async def post_contact():
    return [{"username": "Rick"}, {"username": "Morty"}]
