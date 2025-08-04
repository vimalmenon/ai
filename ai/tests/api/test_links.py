def test_get_links(client, dynamodb_mock) -> None:
    response = client.get("/links")
    assert response.status_code == 200
