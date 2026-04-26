from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class SaleBase(SQLModel):
    total_amount: float
    payment_method: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Sale(SaleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    items: List["SaleItem"] = Relationship(back_populates="sale")

class SaleItemBase(SQLModel):
    sale_id: int = Field(foreign_key="sale.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    unit_price: float
    subtotal: float

class SaleItem(SaleItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale: Sale = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="sales")
