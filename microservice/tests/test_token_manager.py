import pytest
from microservice.services.token_manager import TokenManager

@pytest.fixture
def token_manager():
    return TokenManager()


def test_update_access_token(token_manager):
    access_token = token_manager.update_access_token()
    assert access_token is not None
    assert isinstance(access_token, str)


def test_get_existing_access_token(token_manager, monkeypatch):
    monkeypatch.setattr("time.time", lambda: 1600000000)
    access_token1 = token_manager.get_access_token()
    access_token2 = token_manager.get_access_token()
    assert access_token1 == access_token2


