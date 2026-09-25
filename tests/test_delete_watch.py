from conftest import create_watch

def test_delete_existing_watch(client):
    create_watch(client)

    response = client.delete("/watches/1")

    assert response.status_code == 204


def test_delete_existing_watch_has_no_body(client):
    create_watch(client)

    response = client.delete("/watches/1")

    assert response.status_code == 204
    assert response.data == b""


def test_delete_non_existing_watch(client):
    response = client.delete("/watches/999")

    assert response.status_code == 404


def test_delete_then_get_returns_404(client):
    create_watch(client)

    delete_response = client.delete("/watches/1")

    assert delete_response.status_code == 204

    get_response = client.get("/watches/1")

    assert get_response.status_code == 404


def test_delete_one_watch_does_not_delete_other_watches(client):
    create_watch(client)
    create_watch(client)

    response = client.delete("/watches/1")

    assert response.status_code == 204

    remaining_response = client.get("/watches/2")

    assert remaining_response.status_code == 200

    data = remaining_response.get_json()

    assert data["id"] == 2
