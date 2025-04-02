# File: app/crud/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy import select

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(name=user.name, email=user.email, hashed_password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()
