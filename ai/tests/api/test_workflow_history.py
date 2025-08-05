def test_workflow(client, dynamodb_mock) -> None:
    """
    Test the workflow API endpoints.
    """
    response = client.get("/workflow")
    assert response.status_code == 200
