from conftest import create_watch

def test_multiple_watches_can_be_created_and_retrieved(client):
    create_watch(
        client,
        title="Germany",
        contact_email="germany@example.com",
    )

    create_watch(
        client,
        title="France",
        contact_email="france@example.com",
    )

    create_watch(
        client,
        title="Italy",
        contact_email="italy@example.com",
    )

    response = client.get("/watches")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 3

    assert data[0]["title"] == "Germany"
    assert data[1]["title"] == "France"
    assert data[2]["title"] == "Italy"


def test_update_one_watch_does_not_modify_another(client):
    create_watch(
        client,
        title="Germany",
    )

    create_watch(
        client,
        title="France",
    )

    client.patch(
        "/watches/1",
        json={"title": "Updated Germany"},
    )

    response = client.get("/watches/2")

    data = response.get_json()

    assert data["title"] == "France"


def test_delete_and_update_different_watches(client):
    create_watch(client)
    create_watch(client)

    delete_response = client.delete("/watches/1")

    assert delete_response.status_code == 204

    update_response = client.patch(
        "/watches/2",
        json={"status": "paused"},
    )

    assert update_response.status_code == 200

    data = update_response.get_json()

    assert data["id"] == 2
    assert data["status"] == "paused"


def test_full_watch_lifecycle(client):
    # Create
    create_response = create_watch(client)

    assert create_response.status_code == 201

    created = create_response.get_json()

    watch_id = created["id"]

    # Read
    get_response = client.get(f"/watches/{watch_id}")

    assert get_response.status_code == 200

    # Update
    patch_response = client.patch(
        f"/watches/{watch_id}",
        json={"status": "paused"},
    )

    assert patch_response.status_code == 200

    # Verify update
    updated_response = client.get(
        f"/watches/{watch_id}"
    )

    assert updated_response.status_code == 200

    updated = updated_response.get_json()

    assert updated["status"] == "paused"

    # Delete
    delete_response = client.delete(
        f"/watches/{watch_id}"
    )

    assert delete_response.status_code == 204

    # Verify deletion
    final_response = client.get(
        f"/watches/{watch_id}"
    )

    assert final_response.status_code == 404