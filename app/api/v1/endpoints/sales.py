from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api import deps
from app.models.sale import Sale, SaleItem, SaleBase
from app.models.product import Product, Inventory
from app.models.finance import Finance, TransactionType
from app.models.user import User

router = APIRouter()

class SaleCreateRequest(SaleBase):
    items: List[dict]  # product_id, quantity

@router.post("/", response_model=Sale)
def create_sale(
    *,
    db: Session = Depends(deps.get_session),
    sale_in: SaleCreateRequest,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Process a new sale.
    """
    # 1. Create Sale record
    sale = Sale(total_amount=sale_in.total_amount, payment_method=sale_in.payment_method)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    
    for item_data in sale_in.items:
        product = db.get(Product, item_data["product_id"])
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item_data['product_id']} not found")
        
        # 2. Check and Update Inventory
        inventory = db.exec(select(Inventory).where(Inventory.product_id == product.id)).first()
        if not inventory or inventory.quantity < item_data["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        inventory.quantity -= item_data["quantity"]
        db.add(inventory)
        
        # 3. Create SaleItem
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item_data["quantity"],
            unit_price=product.sale_price,
            subtotal=item_data["quantity"] * product.sale_price
        )
        db.add(sale_item)
    
    # 4. Record in Finance
    finance = Finance(
        amount=sale.total_amount,
        description=f"Sale #{sale.id}",
        transaction_type=TransactionType.INCOME,
        category="sales"
    )
    db.add(finance)
    
    db.commit()
    db.refresh(sale)
    return sale
