from datetime import datetime
from uuid import uuid4

from ai.managers import DbManager
from ai.model import ContactRequestForm
from ai.services.contact_service.contact_db_model import ContactData


class ContactService:

    def create(self, data: ContactRequestForm):
        contact_data = ContactData(
            name="ai#contact",
            id=str(uuid4()),
            title=data.title,
            message=data.message,
            read=False,
            creation_date=datetime.now().isoformat(),
        )
        DbManager().add_item(contact_data.toJSON())
        return contact_data

    def get_items(self):
        return DbManager().query_items("ai#contact")
