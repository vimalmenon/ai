from fastapi import APIRouter

from ai.model import ContactRequestForm

router = APIRouter()


@router.post("/", tags=["contact"])
async def post_contact(data: ContactRequestForm):
    return [{"username": "Rick"}, {"username": "Morty"}]
