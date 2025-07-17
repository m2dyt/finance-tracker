from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, transactions, categories, stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(stats.router)
