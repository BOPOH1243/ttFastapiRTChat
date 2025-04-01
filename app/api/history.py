# File: app/api/history.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.message import get_messages
from app.schemas.message import MessageResponse
from typing import List

router = APIRouter()

@router.get("/history/{chat_id}", response_model=List[MessageResponse])
async def get_history(chat_id: int, limit: int = Query(50, ge=1), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db)):
    messages = await get_messages(db, chat_id=chat_id, limit=limit, offset=offset)
    if messages is None:
        raise HTTPException(status_code=404, detail="Chat not found or no messages")
    return messages
