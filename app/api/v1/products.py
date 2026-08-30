from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        return product_service.create_product(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Product with this SKU already exists")

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductResponse])
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return product_service.list_products(db, skip, limit)