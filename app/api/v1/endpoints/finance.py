from typing import Any, List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.api import deps
from app.models.finance import Finance, TransactionType
from app.models.user import User

router = APIRouter()

@router.get("/summary")
def get_finance_summary(
    db: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get financial summary (Total Gained, Total Spent, Net).
    """
    gains = db.exec(select(func.sum(Finance.amount)).where(Finance.transaction_type == TransactionType.INCOME)).one() or 0
    expenses = db.exec(select(func.sum(Finance.amount)).where(Finance.transaction_type == TransactionType.EXPENSE)).one() or 0
    
    return {
        "total_gained": gains,
        "total_spent": expenses,
        "net_profit": gains - expenses
    }

@router.get("/transactions", response_model=List[Finance])
def read_transactions(
    db: Session = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve financial transactions.
    """
    transactions = db.exec(select(Finance).offset(skip).limit(limit)).all()
    return transactions
