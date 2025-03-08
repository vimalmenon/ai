from pydantic import BaseModel


class ContactRequestForm(BaseModel):
    title: str
    message: str
