from factory import Factory, Faker

from ai.model import Link, LinkGroup, LinkGroupSlim, LinkSlim


class FactoryLinkGroup(Factory):
    class Meta:
        model = LinkGroup

    id = Faker("uuid4")
    name = Faker("text")


class FactoryLink(Factory):
    class Meta:
        model = Link

    id = Faker("uuid4")
    name = Faker("text")
    link = Faker("url")
    reference = Faker("text")


class FactoryLinkSlim(Factory):
    class Meta:
        model = LinkSlim

    name = Faker("text")
    link = Faker("url")
    reference = Faker("text")


class FactoryLinkGroupSlim(Factory):
    class Meta:
        model = LinkGroupSlim

    name = Faker("text")
