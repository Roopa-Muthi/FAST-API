from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.inventory import InventoryCreate
from app.services import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/")
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    return inventory_service.create_inventory(db, payload.product_id, payload.quantity_available)