import os
from collections.abc import Generator
from typing import Any
from unittest.mock import Mock, patch

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


@fixture(scope="function")
def mock_llm_execute_service():
    """
    Fixture to create a mock LLMExecuteService for testing.

    Use this fixture when you need to mock the LLMExecuteService for
    integration tests or when testing code that depends on this service.

    Example:
        def test_my_function(mock_llm_execute_service):
            # Use the mock directly
            mock_llm_execute_service.execute("exec_id", node)
            mock_llm_execute_service.execute.assert_called_once()
    """
    mock_service = Mock()

    # Mock the execute method
    mock_service.execute.return_value = None

    # Mock the execute_llm method
    mock_service.execute_llm.return_value = None

    # Mock the execute_agent method
    mock_service.execute_agent.return_value = None

    return mock_service


@fixture(scope="function")
def mock_llm_execute_service_patch():
    """
    Fixture to patch LLMExecuteService across the application for testing.

    Use this fixture when you want to mock the LLMExecuteService class
    instantiation throughout your application during tests.

    Example:
        def test_my_function(mock_llm_execute_service_patch):
            # Any code that creates LLMExecuteService() will use the mock
            service = LLMExecuteService()  # This will be mocked
            service.execute("exec_id", node)
            mock_llm_execute_service_patch.execute.assert_called_once()
    """
    with patch(
        "ai.services.llm_service.llm_execute_service.LLMExecuteService"
    ) as mock_class:
        mock_instance = Mock()
        mock_instance.execute.return_value = None
        mock_instance.execute_llm.return_value = None
        mock_instance.execute_agent.return_value = None
        mock_class.return_value = mock_instance
        yield mock_instance


@fixture(scope="function")
def mock_llm_service():
    """
    Fixture to mock the LlmService dependency used by LLMExecuteService.

    Use this fixture when testing LLMExecuteService methods directly
    and you want to mock the LLM calls without making real API requests.

    Example:
        def test_llm_execution(mock_llm_service):
            service = LLMExecuteService()
            service.execute_llm("exec_id", node)
            mock_llm_service.return_value.get_llm.assert_called_once()
    """
    with patch("ai.services.llm_service.llm_service.LlmService") as mock_service:
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(
            id="test-id",
            content="Test response",
            response_metadata={"model_name": "test-model"},
        )
        mock_service.return_value.get_llm.return_value = mock_llm
        yield mock_service


@fixture(scope="function")
def mock_ai_message_manager():
    """
    Fixture to mock the AiMessageManager used by LLMExecuteService.

    Use this fixture when testing LLMExecuteService and you want to
    avoid making real database calls to save AI messages.

    Example:
        def test_message_saving(mock_ai_message_manager):
            service = LLMExecuteService()
            service.execute_llm("exec_id", node)
            mock_ai_message_manager.return_value.save_data.assert_called_once()
    """
    with patch(
        "ai.managers.ai_message_manager.ai_message_manager.AiMessageManager"
    ) as mock_manager:
        mock_manager.return_value.save_data.return_value = None
        yield mock_manager
