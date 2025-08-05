def test_get_info(client) -> None:
    """
    Test the get_info API endpoint.
    """
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["env"] == "test"
    assert data["data"]["version"] == "0.0.5t"


def test_llm(client) -> None:
    response = client.get("/llms")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 4
    items = [item for item in data if item["supported"]]
    assert len(items) == 1
