from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, database, oauth

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/categories")
def stats_by_categories(db: Session = Depends(database.get_db), current_user=Depends(oauth.get_current_user)):
    stats = db.query(
        models.Category.name, func.sum(models.Transaction.amount).label("total")
    ).join(models.Transaction).filter(models.Transaction.user_id == current_user.id).group_by(models.Category.name).all()

    return [{"category": c[0], "total": c[1]} for c in stats]
