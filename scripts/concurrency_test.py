import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def place_order(client, label, product_id, quantity):
    payload = {
        "customer_name": f"Concurrent Test {label}",
        "customer_email": f"{label.lower()}@test.com",
        "items": [{"product_id": product_id, "quantity": quantity}],
    }
    response = await client.post(f"{BASE_URL}/orders/", json=payload)
    print(f"[{label}] Status: {response.status_code} | Response: {response.json()}")

async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        await asyncio.gather(
            place_order(client, "A", product_id=3, quantity=3),
            place_order(client, "B", product_id=3, quantity=3),
        )

if __name__ == "__main__":
    asyncio.run(main())