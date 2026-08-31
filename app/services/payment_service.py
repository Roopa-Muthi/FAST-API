from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.payment_event import PaymentEvent
from app.models.order import Order

def process_webhook_event(db: Session, payload):
    # Idempotency check: has this exact event already been processed?
    existing = db.query(PaymentEvent).filter(PaymentEvent.event_id == payload.event_id).first()
    if existing:
        return {"status": "duplicate_ignored", "event_id": payload.event_id}

    # Record the event FIRST (or handle race via unique constraint below)
    event = PaymentEvent(
        event_id=payload.event_id,
        order_id=payload.order_id,
        event_type=payload.event_type,
    )

    try:
        db.add(event)
        db.flush()  # triggers unique constraint check early
    except IntegrityError:
        db.rollback()
        # Another concurrent request already inserted this event_id — treat as duplicate
        return {"status": "duplicate_ignored", "event_id": payload.event_id}

    # Now actually apply the business effect, based on event type
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        db.rollback()
        return {"status": "error", "detail": "Order not found"}

    if payload.event_type == "payment.succeeded":
        order.status = "paid"
    elif payload.event_type == "payment.failed":
        order.status = "payment_failed"

    db.commit()
    return {"status": "processed", "event_id": payload.event_id, "order_status": order.status}