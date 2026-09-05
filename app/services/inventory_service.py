from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.inventory import Inventory

def create_or_update_inventory(db: Session, product_id: int, quantity: int):
    existing = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if existing:
        existing.quantity_available += quantity  # restock: add to current stock
        db.commit()
        db.refresh(existing)
        return existing

    inv = Inventory(product_id=product_id, quantity_available=quantity, reserved_quantity=0)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

def get_inventory_for_update(db: Session, product_id: int):
    stmt = select(Inventory).where(Inventory.product_id == product_id).with_for_update()
    return db.execute(stmt).scalar_one_or_none()