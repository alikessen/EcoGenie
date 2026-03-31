import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app as eco_app


@pytest.fixture
def app(monkeypatch):
    eco_app.app.config.update(TESTING=True)

    monkeypatch.setattr(eco_app, "get_user_by_id", lambda user_id: {"id": int(user_id), "username": "test"})
    monkeypatch.setattr(eco_app, "save_user_input", lambda **kwargs: None)
    monkeypatch.setattr(eco_app, "get_user_history", lambda user_id: [])

    return eco_app.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_client(client):
    with client.session_transaction() as sess:
        sess["_user_id"] = "1"
        sess["_fresh"] = True
    return client
