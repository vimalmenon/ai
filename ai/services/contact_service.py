from ai.model import ContactRequestForm


class ContactService:

    def create(self, data: ContactRequestForm):
        return [{"title": data.title, "message": data.message}]
