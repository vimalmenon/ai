"""Test cases for error handling in the FastAPI application."""

import json
from unittest.mock import Mock, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError


def test_http_exception_handling(client: TestClient) -> None:
    """Test that HTTPException is handled correctly."""
    # Try to access a non-existent endpoint to trigger 404
    response = client.get("/non-existent-endpoint")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data  # FastAPI's default 404 response


def test_http_exception_with_custom_detail(client: TestClient) -> None:
    """Test HTTP exception with custom detail message."""
    # Test a specific endpoint that might raise HTTPException
    # This would require mocking an endpoint that raises HTTPException
    with patch("ai.apis.router_rest") as mock_router:
        # Mock an endpoint that raises HTTPException
        mock_router.get.side_effect = HTTPException(
            status_code=400, detail="Custom error message"
        )

        # The actual test would depend on your specific endpoints
        # This is a pattern for testing custom HTTP exceptions


def test_general_exception_handling():
    """Test that general exceptions are handled correctly."""
    import asyncio

    from fastapi import Request

    from ai.config.env import Env
    from main import general_exception_handler

    # Create a mock request
    mock_request = Mock(spec=Request)

    # Create a test exception
    test_exception = Exception("Test error message")

    # Call the exception handler directly
    async def run_test():
        response = await general_exception_handler(mock_request, test_exception)

        assert response.status_code == 500
        response_data = json.loads(response.body.decode())
        assert response_data["error"] == "Internal Server Error"

        # Check message based on debug mode
        env = Env()
        if env.debug:
            assert response_data["message"] == "Test error message"
        else:
            assert response_data["message"] == "An unexpected error occurred"

    # Run the async test
    asyncio.run(run_test())


def test_pydantic_validation_exception_handling():
    """Test that Pydantic ValidationError is handled correctly."""
    import asyncio

    from fastapi import Request
    from pydantic import BaseModel, Field

    from main import pydantic_validation_exception_handler

    # Create a mock request
    mock_request = Mock(spec=Request)

    # Create a test Pydantic model to generate ValidationError
    class TestModel(BaseModel):
        name: str = Field(..., min_length=1)
        age: int = Field(..., gt=0)

    async def run_test():
        try:
            TestModel(name="", age=-1)  # This should raise ValidationError
        except ValidationError as e:
            # Call the exception handler directly
            response = await pydantic_validation_exception_handler(mock_request, e)

            assert response.status_code == 422
            response_data = json.loads(response.body.decode())
            assert response_data["error"] == "Validation Error"
            assert response_data["message"] == "Data validation failed"
            assert "details" in response_data
            assert isinstance(response_data["details"], list)

    # Run the async test
    asyncio.run(run_test())


def test_request_validation_exception_handling():
    """Test that RequestValidationError is handled correctly."""
    import asyncio

    from fastapi import Request
    from fastapi.exceptions import RequestValidationError

    from main import validation_exception_handler

    # Create a mock request
    mock_request = Mock(spec=Request)

    # Create a test RequestValidationError
    validation_errors = [
        {
            "loc": ("body", "name"),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]

    request_validation_error = RequestValidationError(validation_errors)

    async def run_test():
        # Call the exception handler directly
        response = await validation_exception_handler(
            mock_request, request_validation_error
        )

        assert response.status_code == 422
        response_data = json.loads(response.body.decode())
        assert response_data["error"] == "Validation Error"
        assert response_data["message"] == "Request validation failed"
        # The error handler might convert tuples to lists, so check both
        assert len(response_data["details"]) == 1
        detail = response_data["details"][0]
        assert detail["msg"] == "field required"
        assert detail["type"] == "value_error.missing"
        # loc might be either tuple or list after serialization
        assert detail["loc"] in [["body", "name"], ("body", "name")]

    # Run the async test
    asyncio.run(run_test())


def test_camel_to_snake_middleware_with_invalid_json(client: TestClient) -> None:
    """Test that the camel to snake middleware handles invalid JSON gracefully."""
    # Send a PUT request with invalid JSON to test middleware error handling
    response = client.put(
        "/links",
        content='{"camelCase": "value", "invalid": json}',  # Invalid JSON
        headers={"Content-Type": "application/json"},
    )

    # The middleware should handle the JSONDecodeError gracefully
    # and the request should still be processed (though it might fail validation)
    assert response.status_code in [400, 422]


def test_camel_to_snake_middleware_with_valid_json(client: TestClient) -> None:
    """Test that the camel to snake middleware works correctly with valid JSON."""
    # Send a PUT request with camelCase JSON
    response = client.put(
        "/links",
        json={
            "linkName": "Test Link Group",  # camelCase
        },
        headers={"Content-Type": "application/json"},
    )

    # Should process the request (might fail validation but not due to JSON parsing)
    assert response.status_code in [200, 201, 422]  # Various possible responses


def test_cors_middleware_with_error(client: TestClient) -> None:
    """Test that CORS middleware works even when errors occur."""
    # Make a request that will trigger an error
    response = client.put(
        "/links",
        json={},  # Empty JSON to trigger validation error
        headers={"Content-Type": "application/json", "Origin": "http://localhost:3000"},
    )

    # Should have CORS headers even with error response
    assert response.status_code == 422
    # Check if CORS headers are present (they should be due to middleware)
    assert (
        "access-control-allow-origin" in response.headers
        or "Access-Control-Allow-Origin" in response.headers
    )


def test_error_response_format_consistency(client: TestClient) -> None:
    """Test that all error responses follow the same format."""
    # Test validation error format
    response = client.put("/links", json={})
    assert response.status_code == 422

    data = response.json()
    assert "error" in data
    assert "message" in data
    assert isinstance(data["error"], str)
    assert isinstance(data["message"], str)

    # Test 404 error (different format but should be handled)
    response = client.get("/non-existent")
    assert response.status_code == 404


def test_logging_on_errors(client: TestClient, caplog) -> None:
    """Test that errors are properly logged."""
    import logging

    # Set logging level to capture error logs
    caplog.set_level(logging.ERROR)

    # Trigger a validation error
    response = client.put("/links", json={})
    assert response.status_code == 422

    # Check if error was logged
    assert len(caplog.records) > 0
    assert any(
        "validation error" in record.message.lower() for record in caplog.records
    )


def test_successful_request_with_valid_data(client: TestClient, dynamodb_mock) -> None:
    """Test that valid requests work correctly and don't trigger error handlers."""
    # Send a valid request to create a link group
    # This test uses the dynamodb_mock fixture to avoid real AWS calls
    response = client.put(
        "/links",
        json={"name": "Test Link Group"},
        headers={"Content-Type": "application/json"},
    )

    # Should succeed (or fail due to business logic, not validation)
    # The exact status depends on your business logic, but it shouldn't be 422
    assert response.status_code != 422
    # Could be 200, 201, or some other business logic error but not validation error


def test_validation_error_details_structure(client: TestClient) -> None:
    """Test that validation error details have the expected structure."""
    response = client.put("/links", json={})
    assert response.status_code == 422

    data = response.json()
    assert "details" in data
    details = data["details"]
    assert isinstance(details, list)
    assert len(details) > 0

    # Check that each detail has expected fields
    for detail in details:
        assert "loc" in detail
        assert "msg" in detail
        assert "type" in detail
