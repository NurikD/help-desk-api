from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate  # Импортируем Pydantic-схему
from app.utils.hashing import hash_password

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка, есть ли пользователь
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже используется")
    
    # Хешируем пароль
    hashed_password = hash_password(user.password)

    # Создание нового пользователя
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,  # Сохраняем хешированный пароль
        phone=user.phone,
        company=None  # Если company не передаётся
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Пользователь зарегистрирован", "user_id": new_user.id}

