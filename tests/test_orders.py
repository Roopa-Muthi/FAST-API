def _setup_product_with_stock(client, sku="ORD-SKU", stock=10):
    product_res = client.post("/products/", json={
        "name": "Order Test Product", "sku": sku, "price": 100.00
    })
    product_id = product_res.json()["id"]
    client.post("/inventory/", json={"product_id": product_id, "quantity_available": stock})
    return product_id


def test_create_order_success(client):
    product_id = _setup_product_with_stock(client)
    response = client.post("/orders/", json={
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "items": [{"product_id": product_id, "quantity": 2}]
    })
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"


def test_order_fails_when_insufficient_stock(client):
    product_id = _setup_product_with_stock(client, sku="LOW-STOCK", stock=1)
    response = client.post("/orders/", json={
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "items": [{"product_id": product_id, "quantity": 5}]
    })
    assert response.status_code == 409
    assert "Insufficient stock" in response.json()["detail"]


def test_order_fails_for_nonexistent_product(client):
    response = client.post("/orders/", json={
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "items": [{"product_id": 9999, "quantity": 1}]
    })
    assert response.status_code == 404