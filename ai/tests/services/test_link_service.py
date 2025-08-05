import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import LinkService
from ai.tests.factory.link import FactoryLinkGroupSlim, FactoryLinkSlim


def test_link_service_create_group_link(dynamodb_mock) -> None:
    result = LinkService().create_group_link(FactoryLinkGroupSlim.build())
    assert len(result) == 1


def test_link_service_create_link(dynamodb_mock) -> None:
    result = LinkService().create_group_link(FactoryLinkGroupSlim.build())
    result = LinkService().create_link(result[0].id, FactoryLinkSlim.build())
    assert len(result) == 1
    assert len(result[0].links) == 1


def test_link_service_create_link_with_exception(dynamodb_mock) -> None:
    with pytest.raises(ClientError):
        LinkService().create_link("non_existent_group_id", FactoryLinkSlim.build())
