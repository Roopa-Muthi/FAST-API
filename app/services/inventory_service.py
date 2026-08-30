from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.inventory import Inventory

def create_inventory(db: Session, product_id: int, quantity: int):
    inv = Inventory(product_id=product_id, quantity_available=quantity, reserved_quantity=0)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

def get_inventory_for_update(db: Session, product_id: int):
    """Locks the inventory row until the transaction commits — prevents race conditions."""
    stmt = select(Inventory).where(Inventory.product_id == product_id).with_for_update()
    return db.execute(stmt).scalar_one_or_none()