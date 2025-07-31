from typing import Self

from ai.model.base_model import Base


class LinkSlim(Base):
    name: str
    link: str


class Link(LinkSlim):
    id: str
    name: str
    link: str

    @classmethod
    def to_cls(cls, data: dict[str, str]) -> Self:
        return cls(id=data["id"], name=data["name"], link=data["link"])

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "link": self.link}


class LinkGroupSlim(Base):
    name: str
    links: list[Link]


class LinkGroup(LinkGroupSlim):
    id: str

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
