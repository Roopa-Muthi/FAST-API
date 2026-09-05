from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import products, inventory, orders, payments

app = FastAPI(title="Order & Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(payments.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}