import pytest
from unittest.mock import patch, MagicMock
from microservice.services.products import register_product_in_offer_service


@pytest.fixture
def mock_requests_post():
    with patch('requests.post') as mock_post:
        yield mock_post


def test_register_product_success(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_requests_post.return_value = mock_response

    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6ImZmZjQ3ZmFmLTJlZjUtNDhjZi1iNDg5LTg2NTY1ZDcyODhiMiIsImV4cGlyZXMiOjE2OTQ2NTIxNzN9.Xz70qBGlHE86swmS8Vf4q131H04zzb6rl15Op2BJO_4"
    product_info = {
        "id": "ad64e955-c34e-4970-8a93-9b58aa15d063",
        "name": "Test Product",
        "description": "This is a test product."
    }

    result = register_product_in_offer_service(access_token, product_info)

    assert result is True


def test_register_product_failure(mock_requests_post):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.content.decode.return_value = "Error message"
    mock_requests_post.return_value = mock_response

    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6ImZmZjQ3ZmFmLTJlZjUtNDhjZi1iNDg5LTg2NTY1ZDcyODhiMiIsImV4cGlyZXMiOjE2OTQ2NTIxNzN9.Xz70qBGlHE86swmS8Vf4q131H04zzb6rl15Op2BJO_4"
    product_info = {
        "id": "ad64e955-c34e-4970-8a93-9b58aa15d063",
        "name": "Test Product",
        "description": "This is a test product."
    }

    result = register_product_in_offer_service(access_token, product_info)

    assert result is False
