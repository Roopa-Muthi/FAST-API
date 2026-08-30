from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: Decimal
    description: Optional[str] = None

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    price: Decimal
    description: Optional[str] = None