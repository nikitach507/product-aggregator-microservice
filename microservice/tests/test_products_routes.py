from fastapi.testclient import TestClient
from uuid import UUID
from microservice.main import app

client = TestClient(app)


def test_create_product():
    data = {
        "name": "Test Product",
        "description": "Test Description"
    }
    response = client.post("/products/", json=data)
    assert response.status_code == 200
    product = response.json()
    assert "id" in product
    assert product["name"] == data["name"]
    assert product["description"] == data["description"]


def test_get_product():
    response = client.get("/products/22e11812-d3d0-48b5-9c14-b32395bee0f9")
    assert response.status_code == 200
    product = response.json()
    assert isinstance(product["id"], str)
    assert isinstance(UUID(product["id"]), UUID)


def test_update_product():
    data = {
        "name": "Updated Product",
        "description": "Updated Description"
    }
    response = client.put("/products/22e11812-d3d0-48b5-9c14-b32395bee0f9", json=data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == data["name"]
    assert updated_product["description"] == data["description"]


def test_delete_product():
    response = client.delete("/products/22e11812-d3d0-48b5-9c14-b32395bee0f9")
    assert response.status_code == 200
    deleted_product = response.json()
    assert "id" in deleted_product
    assert "name" in deleted_product
    assert "description" in deleted_product


def test_get_all_products():
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "description" in product
