from dataclasses import dataclass

from pytest import fixture

from ai.managers.db_manager.db_manager import DbManager
from ai.model.enums import DbKeys


@fixture
def mock_data(faker):
    @dataclass
    class MockData:
        primary: str
        secondary: str
        data: str

    return MockData(primary=faker.uuid4(), secondary=faker.uuid4(), data=faker.text())


def test_add_item_and_get_item(dynamodb_mock, setup_environment, mock_data):
    db_manager = DbManager()
    item = {
        DbKeys.Primary.value: mock_data.primary,
        DbKeys.Secondary.value: mock_data.secondary,
        "data": mock_data.data,
    }
    db_manager.add_item(item)
    retrieved_item = db_manager.get_item(
        {
            DbKeys.Primary.value: mock_data.primary,
            DbKeys.Secondary.value: mock_data.secondary,
        }
    )
    assert retrieved_item == item
