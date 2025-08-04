import os
from collections.abc import Generator
from typing import Any

import boto3
from fastapi.testclient import TestClient
from moto import mock_aws
from pytest import fixture

from ai.config import Env
from ai.model.enums import DbKeys
from main import app


@fixture(autouse=True)
def setup_env(faker) -> None:
    """
    Set up the environment for testing.
    """
    os.environ["SUPPORTED_LLM"] = "OLLAMA"
    os.environ["DEEPSEEK_API_KEY"] = "DEEPSEEK"
    os.environ["GOOGLE_API_KEY"] = faker.pystr()
    os.environ["GOOGLE_CSE_ID"] = faker.pystr()
    os.environ["AWS_TABLE"] = "application"
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["AWS_SECRET_MANAGER"] = faker.pystr()
    os.environ["AWS_CLIENT_ID"] = faker.pystr()
    os.environ["AWS_SECRET"] = faker.pystr()
    os.environ["APP_VERSION"] = "0.0.5t"
    os.environ["APP_ENV"] = "test"


@fixture(scope="function")
def dynamodb_mock(setup_env):
    env = Env()
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName=env.table,
            KeySchema=[
                {"AttributeName": DbKeys.Primary.value, "KeyType": "HASH"},
                {"AttributeName": DbKeys.Secondary.value, "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": DbKeys.Primary.value, "AttributeType": "S"},
                {"AttributeName": DbKeys.Secondary.value, "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        table.wait_until_exists()
        yield table


@fixture(scope="function")
def client(setup_env) -> Generator[TestClient, Any, None]:
    """
    Fixture to create a test client for the FastAPI application.
    """

    client = TestClient(app)
    yield client
