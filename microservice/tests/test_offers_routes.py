from fastapi.testclient import TestClient

from microservice.main import app

client = TestClient(app)


def test_get_all_offers():
    response = client.get("/offers/")

    assert response.status_code == 200

    offers = response.json()
    assert len(offers) >= 0


def test_get_offer_by_id():
    offer_id = "1bce5eed-c72d-749a-5572-598216b33f22"
    response = client.get(f"/offers/{offer_id}")

    assert response.status_code == 200

    offer = response.json()
    assert offer["id"] == offer_id


def test_get_offers_by_product_id():
    product_id = "ad63e955-c34e-4970-8a93-9b58aa15d063"
    response = client.get(f"/offers/products/{product_id}")

    assert response.status_code == 200

    offers = response.json()
    assert len(offers) >= 0
