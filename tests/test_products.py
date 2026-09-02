def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Test Mouse",
        "sku": "TEST-001",
        "price": 500.00,
        "description": "A test product"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Mouse"
    assert data["sku"] == "TEST-001"


def test_create_duplicate_sku_fails(client):
    payload = {"name": "Dup", "sku": "DUP-001", "price": 100.00}
    client.post("/products/", json=payload)
    response = client.post("/products/", json=payload)
    assert response.status_code == 409


def test_get_nonexistent_product_returns_404(client):
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_list_products(client):
    client.post("/products/", json={"name": "P1", "sku": "P1-SKU", "price": 100.00})
    client.post("/products/", json={"name": "P2", "sku": "P2-SKU", "price": 200.00})
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2