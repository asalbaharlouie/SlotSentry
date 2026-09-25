import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app, state


@pytest.fixture
def client():
    app.config["TESTING"] = True

    state["watches"].clear()
    state["current_id"] = 1

    with app.test_client() as client:
        yield client

    state["watches"].clear()
    state["current_id"] = 1


def create_watch(client, **overrides):
    data = {
        "title": "نوبت سفارت آلمان",
        "check_interval_minutes": 15,
        "contact_email": "test@example.com",
    }

    data.update(overrides)

    return client.post("/watches", json=data)
