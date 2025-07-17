from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, oauth

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=List[schemas.TransactionOut])
def get_transactions(db: Session = Depends(database.get_db), current_user=Depends(oauth.get_current_user)):
    return db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()

@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionBase, db: Session = Depends(database.get_db),
                       current_user=Depends(oauth.get_current_user)):
    new_transaction = models.Transaction(user_id=current_user.id, **transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
