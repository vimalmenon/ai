from fastapi.testclient import TestClient

from main import app


def test_workflow_history(client) -> None:
    """
    Test the workflow API endpoints.
    """
    response = client.get("/workflow/history/")
    assert response.status_code == 200
