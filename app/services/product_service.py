import json
from sqlalchemy.orm import Session
from app.models.product import Product
from app.db.redis_client import redis_client

CACHE_TTL = 60 # seconds

def get_product(db: Session, product_id: int):
    cache_key = f"product:{product_id}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    data = {
        "id": product.id,
        "name": product.name,
        "sku": product.sku,
        "price": str(product.price),
        "description": product.description,
    }
    redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL)
    return data

def create_product(db: Session, product_data):
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def list_products(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Product).offset(skip).limit(limit).all()

def invalidate_product_cache(product_id: int):
    redis_client.delete(f"product:{product_id}")