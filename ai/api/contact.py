from fastapi import APIRouter

from ai.model import ContactRequestForm
from ai.services import ContactService

router = APIRouter()


@router.post("/", tags=["contact"])
async def post_contact(data: ContactRequestForm):
    """This Add contact"""
    return ContactService().add_item(data)


@router.get("/", tags=["contact"])
async def get_contacts():
    """This List out all contact details"""
    return ContactService().get_items()


@router.delete("/{id}", tags=["contact"])
async def delete_contact(id: str):
    """This will delete contact based on id"""
    return ContactService().delete_item(id)
