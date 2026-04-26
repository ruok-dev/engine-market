from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api import deps
from app.models.product import Inventory, Product
from app.models.finance import Finance, TransactionType
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Inventory])
def read_inventory(
    db: Session = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve inventory status.
    """
    inventory = db.exec(select(Inventory).offset(skip).limit(limit)).all()
    return inventory

@router.post("/replenish", response_model=Inventory)
def replenish_stock(
    *,
    db: Session = Depends(deps.get_session),
    product_id: int,
    quantity: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Manually replenish stock and record expense.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    inventory = db.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if not inventory:
        inventory = Inventory(product_id=product_id, quantity=0)
    
    inventory.quantity += quantity
    db.add(inventory)
    
    # Record expense
    cost = quantity * product.base_price
    finance = Finance(
        amount=cost,
        description=f"Restock: {product.name} (x{quantity})",
        transaction_type=TransactionType.EXPENSE,
        category="purchases"
    )
    db.add(finance)
    
    db.commit()
    db.refresh(inventory)
    return inventory
