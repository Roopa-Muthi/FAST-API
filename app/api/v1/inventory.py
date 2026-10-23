from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.inventory import InventoryCreate
from app.services import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/")
def create_or_update_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    return inventory_service.create_or_update_inventory(db, payload.product_id, payload.quantity_available)

@router.get("/{product_id}")
def check_availability(product_id: int, db: Session = Depends(get_db)):
    inv = inventory_service.get_inventory(db, product_id)
    if not inv:
        raise HTTPException(status_code=404, detail="No inventory record for this product")
    available = inv.quantity_available - inv.reserved_quantity
    return {"product_id": product_id, "available": available}