from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class FinanceBase(SQLModel):
    amount: float
    description: str
    transaction_type: TransactionType
    category: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Finance(FinanceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
