from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.session import Base

class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, nullable=False, index=True)  # idempotency key from provider
    order_id = Column(Integer, nullable=True)
    event_type = Column(String, nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())