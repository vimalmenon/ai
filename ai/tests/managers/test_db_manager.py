from dataclasses import dataclass

from boto3.dynamodb.conditions import Key
from pytest import fixture

from ai.managers.db_manager.db_manager import DbManager
from ai.model.enums import DbKeys


@dataclass
class MockData:
    primary: str
    secondary: str
    data: str


@fixture
def mock_data(faker) -> MockData:
    return MockData(primary=faker.uuid4(), secondary=faker.uuid4(), data=faker.text())


def test_add_item_and_get_item(dynamodb_mock, setup_environment, mock_data) -> None:
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


def test_remove_item(dynamodb_mock, setup_environment, mock_data) -> None:
    db_manager = DbManager()
    item = {
        DbKeys.Primary.value: mock_data.primary,
        DbKeys.Secondary.value: mock_data.secondary,
        "data": mock_data.data,
    }
    db_manager.add_item(item)
    db_manager.remove_item(
        {
            DbKeys.Primary.value: mock_data.primary,
            DbKeys.Secondary.value: mock_data.secondary,
        }
    )
    retrieved_item = db_manager.get_item(
        {
            DbKeys.Primary.value: mock_data.primary,
            DbKeys.Secondary.value: mock_data.secondary,
        }
    )
    assert retrieved_item is None


def test_query_items(dynamodb_mock, setup_environment, mock_data) -> None:
    db_manager = DbManager()
    item = {
        DbKeys.Primary.value: mock_data.primary,
        DbKeys.Secondary.value: mock_data.secondary,
        "data": mock_data.data,
    }
    db_manager.add_item(item)
    items = db_manager.query_items(Key(DbKeys.Primary.value).eq(mock_data.primary))
    assert len(items) == 1
    assert items[0] == item


def test_update_item(dynamodb_mock, setup_environment, mock_data) -> None:
    db_manager = DbManager()
    item = {
        DbKeys.Primary.value: mock_data.primary,
        DbKeys.Secondary.value: mock_data.secondary,
        "data": mock_data.data,
    }
    db_manager.add_item(item)

    updated_data = "Updated data"
    db_manager.update_item(
        Key={
            DbKeys.Primary.value: mock_data.primary,
            DbKeys.Secondary.value: mock_data.secondary,
        },
        UpdateExpression="SET #data = :val",
        ExpressionAttributeValues={":val": updated_data},
        ExpressionAttributeNames={"#data": "data"},
    )

    retrieved_item = db_manager.get_item(
        {
            DbKeys.Primary.value: mock_data.primary,
            DbKeys.Secondary.value: mock_data.secondary,
        }
    )
    assert retrieved_item["data"] == updated_data
