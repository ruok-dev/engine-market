from sqlmodel import Session, select
from app.worker import celery_app
from app.core.db import engine
from app.models.product import Inventory, Product
from app.models.finance import Finance, TransactionType
import logging

@celery_app.task
def check_low_stock():
    """
    Check for products below the minimum threshold and auto-replenish if enabled.
    """
    with Session(engine) as db:
        statement = select(Inventory).where(Inventory.quantity <= Inventory.min_threshold).where(Inventory.is_auto_replenish == True)
        low_stock_items = db.exec(statement).all()
        
        for item in low_stock_items:
            product = db.get(Product, item.product_id)
            replenish_amount = item.min_threshold * 2  # Replenish to double the threshold
            
            # 1. Update stock
            item.quantity += replenish_amount
            db.add(item)
            
            # 2. Record expense
            cost = replenish_amount * product.base_price
            finance = Finance(
                amount=cost,
                description=f"Auto-Replenish: {product.name} (x{replenish_amount})",
                transaction_type=TransactionType.EXPENSE,
                category="purchases"
            )
            db.add(finance)
            
            logging.info(f"Auto-replenished {product.name} with {replenish_amount} units.")
        
        db.commit()
