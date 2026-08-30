from pydantic import BaseModel

class InventoryCreate(BaseModel):
    product_id: int
    quantity_available: int