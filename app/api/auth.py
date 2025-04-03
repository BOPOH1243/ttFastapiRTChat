# File: app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.schemas.user import UserCreate, User
from app.schemas.auth import Token, LoginForm
from app.crud.user import crud_user
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Проверка существования пользователя
    existing_user = await crud_user.get_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Хеширование пароля и создание пользователя
    hashed_password = get_password_hash(user_data.password)
    db_user = await crud_user.create(db, {
        "email": user_data.email,
        "name": user_data.name,
        "hashed_password": hashed_password
    })
    
    return db_user

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginForm = Body(...),  # Используем схему и Body
    db: AsyncSession = Depends(get_db)
):
    user = await crud_user.get_by_email(db, login_data.email)
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}