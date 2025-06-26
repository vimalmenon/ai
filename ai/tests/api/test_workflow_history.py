def test_workflow(client) -> None:
    """
    Test the workflow API endpoints.
    """
    response = client.get("https://testserver/workflow")
    assert response.status_code == 200
