from fastapi import APIRouter

from ai.model import ContactRequestForm
from ai.services import ContactService

router = APIRouter()


@router.post("/", tags=["contact"])
async def post_contact(data: ContactRequestForm):
    return ContactService().create(data)


@router.get("/", tags=["contact"])
async def get_contacts():
    return [{"read": "tests"}]
