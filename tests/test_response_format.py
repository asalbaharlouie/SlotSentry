from conftest import create_watch

def test_create_watch_returns_json(client):
    response = create_watch(client)

    assert response.content_type.startswith("application/json")


def test_get_watch_returns_json(client):
    create_watch(client)

    response = client.get("/watches/1")

    assert response.content_type.startswith("application/json")


def test_list_watches_returns_json(client):
    response = client.get("/watches")

    assert response.content_type.startswith("application/json")


def test_patch_returns_json(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={"status": "paused"},
    )

    assert response.content_type.startswith("application/json")


def test_error_response_returns_json(client):
    response = client.get("/watches/999")

    assert response.content_type.startswith("application/json")