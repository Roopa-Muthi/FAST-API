def _create_order(client):
    product_res = client.post("/products/", json={
        "name": "Webhook Test Product", "sku": "WH-SKU", "price": 50.00
    })
    product_id = product_res.json()["id"]
    client.post("/inventory/", json={"product_id": product_id, "quantity_available": 10})
    order_res = client.post("/orders/", json={
        "customer_name": "Webhook Tester",
        "customer_email": "webhook@example.com",
        "items": [{"product_id": product_id, "quantity": 1}]
    })
    return order_res.json()["id"]


def test_webhook_processes_once(client):
    order_id = _create_order(client)
    payload = {
        "event_id": "evt_pytest_001",
        "event_type": "payment.succeeded",
        "order_id": order_id,
        "amount": 50.00
    }
    response = client.post("/webhooks/payment", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "processed"


def test_duplicate_webhook_is_ignored(client):
    order_id = _create_order(client)
    payload = {
        "event_id": "evt_pytest_dup",
        "event_type": "payment.succeeded",
        "order_id": order_id,
        "amount": 50.00
    }
    first = client.post("/webhooks/payment", json=payload)
    second = client.post("/webhooks/payment", json=payload)

    assert first.json()["status"] == "processed"
    assert second.json()["status"] == "duplicate_ignored"