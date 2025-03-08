from datetime import datetime
from uuid import uuid4

from ai.model import ContactRequestForm
from ai.services.contact_service.contact_db_model import ContactData


class ContactService:

    def create(self, data: ContactRequestForm):
        contact_data = ContactData(
            id=str(uuid4()),
            app="ai#contact",
            title=data.title,
            message=data.message,
            read=False,
            creation_date=datetime.now().isoformat(),
        )
        return contact_data
