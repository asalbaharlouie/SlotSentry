from conftest import create_watch

def test_deleted_id_is_not_reused(client):
    create_watch(client)
    client.delete("/watches/1")

    response = create_watch(client)

    data = response.get_json()

    assert data["id"] == 2


def test_ids_are_unique(client):
    responses = [
        create_watch(client),
        create_watch(client),
        create_watch(client),
    ]

    ids = [
        response.get_json()["id"]
        for response in responses
    ]

    assert len(ids) == len(set(ids))


def test_patch_persists_in_memory_state(client):
    create_watch(client)

    client.patch(
        "/watches/1",
        json={"status": "paused"},
    )

    response = client.get("/watches/1")

    data = response.get_json()

    assert data["status"] == "paused"


def test_delete_removes_from_list(client):
    create_watch(client)
    create_watch(client)

    client.delete("/watches/1")

    response = client.get("/watches")

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["id"] == 2

def test_post_on_single_watch_route_is_not_allowed(client):
    response = client.post("/watches/1")

    assert response.status_code == 405


def test_delete_on_collection_route_is_not_allowed(client):
    response = client.delete("/watches")

    assert response.status_code == 405


def test_patch_on_collection_route_is_not_allowed(client):
    response = client.patch(
        "/watches",
        json={"status": "paused"},
    )

    assert response.status_code == 405


def test_get_unknown_route_returns_404(client):
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
