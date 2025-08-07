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


def test_add_item_and_get_item(dynamodb_mock, mock_data) -> None:
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


def test_remove_item(dynamodb_mock, mock_data) -> None:
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


def test_query_items(dynamodb_mock, mock_data) -> None:
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


def test_update_item(dynamodb_mock, mock_data) -> None:
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


def test_batch_get_item_success(dynamodb_mock, faker) -> None:
    """Test batch_get_item returns items for valid keys."""
    db_manager = DbManager()

    # Create test items
    item1 = {
        DbKeys.Primary.value: faker.uuid4(),
        DbKeys.Secondary.value: faker.uuid4(),
        "data": faker.text(),
    }
    item2 = {
        DbKeys.Primary.value: faker.uuid4(),
        DbKeys.Secondary.value: faker.uuid4(),
        "data": faker.text(),
    }

    # Add items to the database
    db_manager.add_item(item1)
    db_manager.add_item(item2)

    # Prepare keys for batch get
    keys = [
        {
            DbKeys.Primary.value: item1[DbKeys.Primary.value],
            DbKeys.Secondary.value: item1[DbKeys.Secondary.value],
        },
        {
            DbKeys.Primary.value: item2[DbKeys.Primary.value],
            DbKeys.Secondary.value: item2[DbKeys.Secondary.value],
        },
    ]

    # Test batch_get_item
    result = db_manager.batch_get_item(keys)

    assert result is not None
    assert "Responses" in result
    responses = result["Responses"]
    assert len(responses) == 1  # One table name in responses

    # Get the table name and check items
    table_name = list(responses.keys())[0]
    items = responses[table_name]
    assert len(items) == 2

    # Verify items are returned correctly
    returned_items = sorted(items, key=lambda x: x[DbKeys.Primary.value])
    expected_items = sorted([item1, item2], key=lambda x: x[DbKeys.Primary.value])
    assert returned_items == expected_items


def test_batch_get_item_partial_success(dynamodb_mock, faker) -> None:
    """Test batch_get_item returns only existing items when some keys don't exist."""
    db_manager = DbManager()

    # Create and add only one item
    existing_item = {
        DbKeys.Primary.value: faker.uuid4(),
        DbKeys.Secondary.value: faker.uuid4(),
        "data": faker.text(),
    }
    db_manager.add_item(existing_item)

    # Prepare keys: one existing, one non-existing
    keys = [
        {
            DbKeys.Primary.value: existing_item[DbKeys.Primary.value],
            DbKeys.Secondary.value: existing_item[DbKeys.Secondary.value],
        },
        {
            DbKeys.Primary.value: faker.uuid4(),  # Non-existing item
            DbKeys.Secondary.value: faker.uuid4(),
        },
    ]

    # Test batch_get_item
    result = db_manager.batch_get_item(keys)

    assert result is not None
    assert "Responses" in result
    responses = result["Responses"]

    # Get the table name and check items
    table_name = list(responses.keys())[0]
    items = responses[table_name]
    assert len(items) == 1  # Only one item should be returned
    assert items[0] == existing_item


def test_batch_get_item_empty_keys(dynamodb_mock) -> None:
    """Test batch_get_item with empty keys list."""
    db_manager = DbManager()

    result = db_manager.batch_get_item([])

    assert result is not None
    assert "Responses" in result


def test_batch_get_item_nonexistent_keys(dynamodb_mock, faker) -> None:
    """Test batch_get_item with keys that don't exist in the database."""
    db_manager = DbManager()

    # Prepare keys for items that don't exist
    keys = [
        {
            DbKeys.Primary.value: faker.uuid4(),
            DbKeys.Secondary.value: faker.uuid4(),
        },
        {
            DbKeys.Primary.value: faker.uuid4(),
            DbKeys.Secondary.value: faker.uuid4(),
        },
    ]

    # Test batch_get_item
    result = db_manager.batch_get_item(keys)

    assert result is not None
    assert "Responses" in result
    responses = result["Responses"]

    # Get the table name and check no items are returned
    table_name = list(responses.keys())[0]
    items = responses[table_name]
    assert len(items) == 0


def test_batch_get_item_client_error(dynamodb_mock, faker) -> None:
    """Test batch_get_item handles ClientError by returning None."""
    from unittest.mock import patch

    from botocore.exceptions import ClientError

    db_manager = DbManager()

    # Prepare test keys
    keys = [
        {
            DbKeys.Primary.value: faker.uuid4(),
            DbKeys.Secondary.value: faker.uuid4(),
        }
    ]

    # Mock the DynamoDB batch_get_item to raise ClientError
    with patch.object(db_manager.dynamodb, "batch_get_item") as mock_batch_get:
        mock_batch_get.side_effect = ClientError(
            error_response={
                "Error": {"Code": "ValidationException", "Message": "Test error"}
            },
            operation_name="BatchGetItem",
        )

        result = db_manager.batch_get_item(keys)
        assert result is None
