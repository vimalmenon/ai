from datetime import datetime
from uuid import uuid4

from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import ContactRequestForm
from ai.services.contact_service.contact_db_model import ContactData


class ContactService:
    def __init__(self):
        self._name = "ai#contact"

    def create(self, data: ContactRequestForm):
        contact_data = ContactData(
            name=self._name,
            id=str(uuid4()),
            title=data.title,
            message=data.message,
            read=False,
            creation_date=datetime.now().isoformat(),
        )
        DbManager().add_item(contact_data.toJSON())
        return contact_data

    def get_items(self):
        return DbManager().query_items(Key("name").eq(self._name))

    def delete_item(self, id: str):
        return DbManager().remove_item({"name": self._name, "id": id})
