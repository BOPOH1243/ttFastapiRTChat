from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate

class CRUDUser:
    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create(self, db: AsyncSession, user_data: dict) -> User:
        db_user = User(
            email=user_data["email"],
            name=user_data["name"],
            hashed_password=user_data["hashed_password"]
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

crud_user = CRUDUser()