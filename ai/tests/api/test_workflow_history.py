from fastapi.testclient import TestClient

from main import app


def test_workflow_history() -> None:
    """
    Test the workflow API endpoints.
    """
    client = TestClient(
        app,
        base_url="http://testserver",
        raise_server_exceptions=True,
        backend="asyncio",
        follow_redirects=True,
    )
    response = client.get("/workflow/history/")
    assert response.status_code == 200
