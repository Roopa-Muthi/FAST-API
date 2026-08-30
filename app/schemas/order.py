from pydantic import BaseModel
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    status: str
    customer_name: str
    customer_email: str

    class Config:
        from_attributes = True