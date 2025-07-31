from ai.managers import LinkManager
from ai.model import Link, LinkGroup, LinkGroupSlim, LinkSlim
from ai.utilities import generate_uuid


class LinkService:

    def create_group_link(self, data: LinkGroupSlim) -> list[LinkGroup]:
        LinkManager().create_group_link(
            LinkGroup(id=generate_uuid(), name=data.name, links=[])
        )
        return LinkManager().get_links()

    def create_link(self, id: str, data: LinkSlim) -> list[LinkGroup]:
        manager = LinkManager()
        result = manager.get_group_link_by_id(id)
        result.links.append(
            Link(
                id=generate_uuid(),
                name=data.name,
                link=data.link,
                reference=data.reference,
            )
        )
        manager.update_group_link(result)
        return LinkManager().get_links()

    def delete_link(self, id: str) -> None:
        LinkManager().delete_link_group(id)

    def delete_group_link(self, id: str):
        pass

    def get_links(self) -> list[LinkGroup]:
        return LinkManager().get_links()
