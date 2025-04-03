from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.group import Group, group_users

class CRUDGroup:
    async def create(self, db: AsyncSession, group_data) -> Group:
        db_group = Group(**group_data.dict())
        db.add(db_group)
        await db.commit()
        await db.refresh(db_group)
        return db_group

    async def add_participant(self, db: AsyncSession, group_id: int, user_id: int):
        stmt = insert(group_users).values(group_id=group_id, user_id=user_id)
        await db.execute(stmt)
        await db.commit()

    async def remove_participant(self, db: AsyncSession, group_id: int, user_id: int):
        stmt = delete(group_users).where(
            (group_users.c.group_id == group_id) &
            (group_users.c.user_id == user_id)
        )
        await db.execute(stmt)
        await db.commit()

    async def get_group_with_participants(self, db: AsyncSession, group_id: int):
        result = await db.execute(
            select(Group)
            .options(selectinload(Group.participants))
            .filter(Group.id == group_id)
        )
        return result.scalars().first()

crud_group = CRUDGroup()