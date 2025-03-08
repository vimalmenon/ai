from fastapi import APIRouter

from ai.model import ContactRequestForm
from ai.services import ContactService

router = APIRouter()


@router.post("/", tags=["contact"])
async def post_contact(data: ContactRequestForm):
    return ContactService().create(data)


@router.get("/", tags=["contact"])
async def get_contacts():
    return ContactService().get_items()


@router.delete("/{id}", tags=["contact"])
async def delete_contact(id: str):
    return ContactService().delete_item(id)
