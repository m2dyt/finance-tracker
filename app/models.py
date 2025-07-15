from sqlalchemy.sql import func 
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, TIMESTAMP
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Numeric(10, 2))
    description = Column(String)
    date = Column(TIMESTAMP, server_default=func.now())
