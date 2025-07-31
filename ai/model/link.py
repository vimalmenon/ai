from typing import Self

from ai.model.base_model import Base


class LinkSlim(Base):
    name: str
    link: str
    reference: str


class Link(LinkSlim):
    id: str

    @classmethod
    def to_cls(cls, data: dict[str, str]) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
            link=data["link"],
            reference=data["reference"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "reference": self.reference,
        }


class LinkGroupSlim(Base):
    name: str


class LinkGroup(LinkGroupSlim):
    id: str
    links: list[Link]

    @classmethod
    def to_cls(cls, data: dict) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
            links=[Link.to_cls(link) for link in data["links"]],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "links": [link.to_dict() for link in self.links],
        }
