# File: app/crud/group.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.group import Group
from app.schemas.group import GroupCreate
from app.models.user import User

async def create_group(db: AsyncSession, group_data: GroupCreate) -> Group:
    db_group = Group(title=group_data.title, creator_id=group_data.creator_id)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    
    # Добавляем участников группы
    if group_data.participant_ids:
        result = await db.execute(select(User).filter(User.id.in_(group_data.participant_ids)))
        users = result.scalars().all()
        db_group.participants.extend(users)
        await db.commit()
    return db_group

async def get_group(db: AsyncSession, group_id: int) -> Group | None:
    result = await db.execute(select(Group).filter(Group.id == group_id))
    return result.scalars().first()
