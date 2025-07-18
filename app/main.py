from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, transactions, categories, stats
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Finance Tracker")

origins = [
    "http://localhost:3000",  # адрес твоего React-приложения
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # разрешаем фронту доступ
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(stats.router)
