from fastapi.testclient import TestClient


def test_get_links(client: TestClient, dynamodb_mock) -> None:
    response = client.get("/links")
    assert response.status_code == 200


def test_request_validation_error_wrong_types(client: TestClient, faker) -> None:
    """Test validation error when field types are wrong."""
    # Send data with wrong types to trigger validation error
    response = client.put(
        "/links",
        json={
            "name": faker.pyint(),  # Should be string
        },
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Error"
    assert data["message"] == "Request validation failed"


def test_request_validation_error(client: TestClient) -> None:
    """Test that RequestValidationError is handled correctly."""
    # Send a PUT request with invalid JSON structure to trigger validation error
    # Using the links endpoint that expects specific fields
    response = client.put(
        "/links",
        json={"invalid_field": "value"},  # Missing required fields
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Error"
    assert data["message"] == "Request validation failed"
    assert "details" in data
    assert isinstance(data["details"], list)


def test_request_validation_error_missing_fields(client: TestClient) -> None:
    """Test validation error when required fields are missing."""
    # Test with completely empty body for link group creation
    response = client.put(
        "/links", json={}, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Error"
    assert data["message"] == "Request validation failed"
    assert "details" in data


def test_invalid_json_format(client: TestClient) -> None:
    """Test handling of invalid JSON format."""
    # Send malformed JSON
    response = client.put(
        "/links",
        content='{"invalid": json}',  # Invalid JSON syntax
        headers={"Content-Type": "application/json"},
    )

    # Should still get a validation error or JSON decode error
    assert response.status_code in [400, 422]
