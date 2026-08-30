from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, payload)