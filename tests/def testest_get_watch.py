def test_get_existing_watch(client):
    create_watch(client)

    response = client.get("/watches/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["title"] == "نوبت سفارت آلمان"


def test_get_non_existing_watch(client):
    response = client.get("/watches/999")

    assert response.status_code == 404

    data = response.get_json()

    assert "response" in data


def test_get_deleted_watch_returns_404(client):
    create_watch(client)

    delete_response = client.delete("/watches/1")

    assert delete_response.status_code == 204

    response = client.get("/watches/1")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "watch_id",
    [
        0,
        -1,
        999,
        1000000,
    ],
)
def test_get_invalid_watch_ids(client, watch_id):
    response = client.get(f"/watches/{watch_id}")

    assert response.status_code == 404

def test_get_all_watches_when_empty(client):
    response = client.get("/watches")

    assert response.status_code == 200

    data = response.get_json()

    assert data == []


def test_get_all_watches(client):
    create_watch(client)

    create_watch(
        client,
        title="نوبت سفارت فرانسه",
        contact_email="france@example.com",
    )

    response = client.get("/watches")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


def test_get_all_watches_contains_expected_fields(client):
    create_watch(client)

    response = client.get("/watches")

    data = response.get_json()

    expected_fields = {
        "id",
        "status",
        "title",
        "check_interval_minutes",
        "contact_email",
    }

    assert set(data[0].keys()) == expected_fields
    