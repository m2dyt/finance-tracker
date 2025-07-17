from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: int
    description: Optional[str]
    date: date
    category_id: int

class TransactionOut(TransactionBase):
    id: int
    created_at: datetime
    category: CategoryOut

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

