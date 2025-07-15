# app/main.py
from fastapi import Form
from app.auth import verify_password
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from .auth import create_access_token, get_password_hash, get_current_user
from .schemas import UserCreate, UserLogin, Token
from .models import User
from .database import get_db

app = FastAPI()

# --- Регистрация ---
@app.post("/register/", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже такого пользователя
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Имя пользователя занято")
    
    # Хешируем пароль и сохраняем пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    
    # Создаем токен
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Вход ---
@app.post("/login/", response_model=Token)
def login(
    username: str = Form(...),  # Принимаем из формы
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Защищенный роут (только для авторизованных) ---
@app.get("/me/")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
