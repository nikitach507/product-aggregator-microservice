import pytest
from unittest.mock import Mock, patch
from microservice.background_service.background_service import BackgroundService


@pytest.fixture
def background_service():
    return BackgroundService()


def test_update_offers_data_without_access_token(background_service):
    mock_token_manager = Mock()
    mock_token_manager.get_access_token.side_effect = Exception("No token")
    background_service.access_token = None
    background_service.token_timestamp = 0

    with patch("microservice.background_service.background_service.token_manager", mock_token_manager):
        with patch(
                "microservice.background_service.background_service.get_product_offer_data") as mock_get_product_offer_data:
            background_service.update_offers_data()

            assert background_service.access_token is None
            assert background_service.token_timestamp == 0
            mock_get_product_offer_data.assert_not_called()


def test_run_periodically(background_service):
    mock_token_manager = Mock()
    mock_token_manager.get_access_token.return_value = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6ImZmZjQ3ZmFmLTJlZjUtNDhjZi1iNDg5LTg2NTY1ZDcyODhiMiIsImV4cGlyZXMiOjE2OTQ2NTIxNzN9.Xz70qBGlHE86swmS8Vf4q131H04zzb6rl15Op2BJO_4"
    background_service.access_token = None
    background_service.token_timestamp = 0

    with patch("microservice.background_service.background_service.token_manager", mock_token_manager):
        with patch(
                "microservice.background_service.background_service.get_product_offer_data") as mock_get_product_offer_data:
            background_service.running = True
            background_service.run_periodically()

            mock_get_product_offer_data.assert_called()
