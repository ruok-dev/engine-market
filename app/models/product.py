from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class ProductBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    sku: str = Field(unique=True, index=True)
    category: str = Field(index=True)
    base_price: float
    sale_price: float

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    inventory: "Inventory" = Relationship(back_populates="product")
    sales: List["SaleItem"] = Relationship(back_populates="product")

class InventoryBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(default=0)
    min_threshold: int = Field(default=10)  # For auto-replenishment
    is_auto_replenish: bool = Field(default=True)

class Inventory(InventoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    product: Product = Relationship(back_populates="inventory")
