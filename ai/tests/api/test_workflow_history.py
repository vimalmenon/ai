def test_workflow_history(client) -> None:
    """
    Test the workflow API endpoints.
    """
    response = client.get("/workflow/history/")
    assert response.status_code == 200
