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
    
    if group_data.participant_ids:
        result = await db.execute(select(User).filter(User.id.in_(group_data.participant_ids)))
        users = result.scalars().all()
        db_group.participants.extend(users)
        await db.commit()
    return db_group

async def get_group(db: AsyncSession, group_id: int) -> Group | None:
    result = await db.execute(select(Group).filter(Group.id == group_id))
    return result.scalars().first()

async def remove_user_from_group(db: AsyncSession, group_id: int, user_id: int) -> Group | None:
    result = await db.execute(select(Group).filter(Group.id == group_id))
    group = result.scalars().first()
    if not group:
        return None
    user_to_remove = None
    for user in group.participants:
        if user.id == user_id:
            user_to_remove = user
            break
    if user_to_remove:
        group.participants.remove(user_to_remove)
        await db.commit()
        return group
    return None
