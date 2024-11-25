from fastapi import FastAPI
from app.database.db import Base, engine
from app.models import models
from app.routes import users

# Инициализация приложения
app = FastAPI()

# Создаём таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Подключение роутов
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Help Desk API is running"}
