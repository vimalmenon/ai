from dataclasses import dataclass


@dataclass
class ContactData:
    id: str
    app: str
    title: str
    message: str
    read: bool
    creation_date: str

    def toJSON(self):
        return self.__dict__
