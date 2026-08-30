from fastapi import FastAPI
from app.api.v1 import products, inventory, orders

app = FastAPI(title="Order & Inventory Management API")

app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(orders.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}