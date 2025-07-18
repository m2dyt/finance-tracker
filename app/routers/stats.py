from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from .. import models, database, oauth

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/categories")
def stats_by_categories(
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth.get_current_user),
    type: Optional[str] = None
):
    query = db.query(
        models.Category.name, func.sum(models.Transaction.amount).label("total")
    ).join(models.Transaction).filter(models.Transaction.user_id == current_user.id)

    if type:
        query = query.filter(models.Transaction.type == type)

    stats = query.group_by(models.Category.name).all()

    return [{"category": c[0], "total": c[1]} for c in stats]

@router.get("/summary")
def stats_summary(
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth.get_current_user)
):
    # Сумма доходов
    income = db.query(func.coalesce(func.sum(models.Transaction.amount), 0))\
        .filter(models.Transaction.user_id == current_user.id, models.Transaction.type == "income").scalar()

    # Сумма расходов
    expense = db.query(func.coalesce(func.sum(models.Transaction.amount), 0))\
        .filter(models.Transaction.user_id == current_user.id, models.Transaction.type == "expense").scalar()

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }
