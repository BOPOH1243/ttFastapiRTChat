# File: app/api/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse
from app.crud.user import get_user_by_id
from app.core.database import get_db
from app.api.chat import oauth2_scheme, get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
