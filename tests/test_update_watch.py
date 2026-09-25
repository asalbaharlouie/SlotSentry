from conftest import create_watch

def test_patch_existing_watch(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={"status": "paused"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "paused"


def test_patch_changes_only_requested_field(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={"status": "paused"},
    )

    data = response.get_json()

    assert data["status"] == "paused"
    assert data["title"] == "نوبت سفارت آلمان"
    assert data["check_interval_minutes"] == 15
    assert data["contact_email"] == "test@example.com"


def test_patch_multiple_fields(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={
            "title": "عنوان جدید",
            "check_interval_minutes": 30,
            "status": "paused",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["title"] == "عنوان جدید"
    assert data["check_interval_minutes"] == 30
    assert data["status"] == "paused"


def test_patch_non_existing_watch(client):
    response = client.patch(
        "/watches/999",
        json={"status": "paused"},
    )

    assert response.status_code == 404


def test_patch_empty_object(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "response" in data


def test_patch_without_json(client):
    create_watch(client)

    response = client.patch("/watches/1")

    assert response.status_code == 400


def test_patch_can_add_unexpected_field(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={"hacked_field": "oops"},
    )

    data = response.get_json()

    assert "hacked_field" not in data


def test_patch_does_not_change_watch_id(client):
    create_watch(client)

    response = client.patch(
        "/watches/1",
        json={"id": 999},
    )

    data = response.get_json()

    assert data["id"] == 1
    