from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.services.inventory_service import get_inventory_for_update
from app.services.product_service import invalidate_product_cache

def create_order(db: Session, payload):
    order = Order(
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        status="pending",
    )
    db.add(order)
    db.flush()  # gets order.id without committing yet

    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        # Locks the inventory row — blocks other concurrent transactions on this product
        inventory = get_inventory_for_update(db, item.product_id)
        if not inventory:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"No inventory record for product {item.product_id}")

        available = inventory.quantity_available - inventory.reserved_quantity
        if available < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"Insufficient stock for product {item.product_id}. Available: {available}, requested: {item.quantity}"
            )

        inventory.quantity_available -= item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
        )
        db.add(order_item)
        invalidate_product_cache(item.product_id)

    order.status = "confirmed"
    db.commit()
    db.refresh(order)
    return order