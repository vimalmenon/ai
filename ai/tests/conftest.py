import os
from collections.abc import Generator
from typing import Any

from fastapi.testclient import TestClient
from pytest import fixture

from main import app


def setup_env() -> None:
    """
    Set up the environment for testing.
    """
    os.environ["SUPPORTED_LLM"] = "OLLAMA"
    os.environ["DEEPSEEK_API_KEY"] = "DEEPSEEK"


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

    client = TestClient(app)
    yield client
