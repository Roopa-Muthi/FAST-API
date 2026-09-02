from pydantic import BaseModel, ConfigDict
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    customer_name: str
    customer_email: str