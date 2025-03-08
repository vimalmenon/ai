from dataclasses import dataclass


@dataclass
class ContactData:
    id: str
    app: str
    title: str
    message: str
    read: bool
    created_at: str
