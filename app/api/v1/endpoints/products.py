from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api import deps
from app.models.product import Product, ProductBase, Inventory
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Product])
def read_products(
    db: Session = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve products.
    """
    products = db.exec(select(Product).offset(skip).limit(limit)).all()
    return products

@router.post("/", response_model=Product)
def create_product(
    *,
    db: Session = Depends(deps.get_session),
    product_in: ProductBase,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new product.
    """
    product = Product.from_orm(product_in)
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Initialize inventory
    inventory = Inventory(product_id=product.id, quantity=0)
    db.add(inventory)
    db.commit()
    
    return product

@router.get("/{id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(deps.get_session),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get product by ID.
    """
    product = db.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
