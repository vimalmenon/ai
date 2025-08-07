from fastapi.testclient import TestClient


def test_workflow(client: TestClient, dynamodb_mock) -> None:
    """
    Test the workflow API endpoints.
    """
    response = client.get("/workflow")
    assert response.status_code == 200
