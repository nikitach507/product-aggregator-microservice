import pytest
from unittest.mock import patch, MagicMock
from microservice.services.offers import get_product_offer_data


@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


def test_get_product_offer_data_success(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"offer_data": "something"}
    mock_requests_get.return_value = mock_response

    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6ImZmZjQ3ZmFmLTJlZjUtNDhjZi1iNDg5LTg2NTY1ZDcyODhiMiIsImV4cGlyZXMiOjE2OTQ2NTIxNzN9.Xz70qBGlHE86swmS8Vf4q131H04zzb6rl15Op2BJO_4"
    product_id = "ad63e955-c34e-4970-8a93-9b58aa15d053"

    result = get_product_offer_data(access_token, product_id)

    assert result == {"offer_data": "something"}


def test_get_product_offer_data_failure(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.content.decode.return_value = "Error message"
    mock_requests_get.return_value = mock_response

    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6ImZmZjQ3ZmFmLTJlZjUtNDhjZi1iNDg5LTg2NTY1ZDcyODhiMiIsImV4cGlyZXMiOjE2OTQ2NTIxNzN9.Xz70qBGlHE86swmS8Vf4q131H04zzb6rl15Op2BJO_4"
    product_id = "ad63e955-c34e-4970-8a93-9b58aa15d053"

    result = get_product_offer_data(access_token, product_id)

    assert result is False
