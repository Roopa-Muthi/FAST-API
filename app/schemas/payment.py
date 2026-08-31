from pydantic import BaseModel
from typing import Optional

class PaymentWebhookPayload(BaseModel):
    event_id: str          # unique idempotency key sent by the payment provider
    event_type: str        # e.g. "payment.succeeded", "payment.failed"
    order_id: int
    amount: Optional[float] = None