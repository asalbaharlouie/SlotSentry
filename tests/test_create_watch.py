import pytest
from conftest import create_watch

def test_create_watch_success(client):
    response = create_watch(client)

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 1
    assert data["status"] == "active"
    assert data["title"] == "نوبت سفارت آلمان"
    assert data["check_interval_minutes"] == 15
    assert data["contact_email"] == "test@example.com"


def test_create_second_watch_gets_incremented_id(client):
    first_response = create_watch(client)
    second_response = create_watch(
        client,
        title="نوبت سفارت فرانسه",
        contact_email="test@example.com",
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_data = first_response.get_json()
    second_data = second_response.get_json()

    assert first_data["id"] == 1
    assert second_data["id"] == 2


def test_create_watch_default_status_is_active(client):
    response = create_watch(client)

    data = response.get_json()

    assert data["status"] == "active"


@pytest.mark.parametrize(
    "missing_field",
    [
        "title",
        "check_interval_minutes",
        "contact_email",
    ],
)
def test_create_watch_missing_required_field(client, missing_field):
    data = {
        "title": "نوبت سفارت آلمان",
        "check_interval_minutes": 15,
        "contact_email": "test@example.com",
    }

    del data[missing_field]

    response = client.post("/watches", json=data)

    assert response.status_code == 400

    response_data = response.get_json()

    assert "response" in response_data
    assert missing_field in response_data["response"]


def test_create_watch_empty_json_object(client):
    response = client.post("/watches", json={})

    assert response.status_code == 400


def test_create_watch_without_json(client):
    response = client.post("/watches")

    assert response.status_code == 400


def test_create_watch_invalid_json(client):
    response = client.post(
        "/watches",
        data="this is not json",
        content_type="application/json",
    )

    assert response.status_code == 400


def test_create_watch_with_extra_fields(client):
    response = create_watch(
        client,
        unexpected_field="should_not_be_here",
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "unexpected_field" not in data
