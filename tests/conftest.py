import os
from typing import Any, Generator
from pytest import fixture
from fastapi.testclient import TestClient

from main import app

def setup_env() -> None:
    """
    Set up the environment for testing.
    """
    os.environ["SUPPORTED_LLM"] = "DEEPSEEK"

@fixture(autouse=True)
def setup_environment() -> None:
    """
    Fixture to set up the environment for testing.
    """
    setup_env()

@fixture(scope="function")
def client(setup_environment) -> Generator[TestClient, Any, None]:
    """
    Fixture to create a test client for the FastAPI application.
    """


    client = TestClient(
        app,
        base_url="http://testserver",
        raise_server_exceptions=True,
        backend="asyncio",
        follow_redirects=True,
    )
    yield client