from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.payment import PaymentWebhookPayload
from app.services import payment_service

router = APIRouter(prefix="/webhooks", tags=["Payments"])

@router.post("/payment")
def payment_webhook(payload: PaymentWebhookPayload, db: Session = Depends(get_db)):
    return payment_service.process_webhook_event(db, payload)