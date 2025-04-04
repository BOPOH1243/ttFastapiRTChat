from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.chat import Chat, ChatCreate, ChatUpdate
from app.crud.chat import crud_chat
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.chat import Chat as ChatModel

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/", response_model=List[Chat])
async def read_chats(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает список чатов с пагинацией.
    """
    chats = await crud_chat.get_multi(db, skip=skip, limit=limit)
    # Преобразование участников в список идентификаторов для ответа.
    for chat in chats:
        chat.participant_ids = [user.id for user in chat.participants] if chat.participants else []
    return chats


@router.get("/{chat_id}", response_model=Chat)
async def read_chat(
    chat_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает данные конкретного чата по идентификатору.
    """
    db_chat = await crud_chat.get(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    db_chat.participant_ids = [user.id for user in db_chat.participants] if db_chat.participants else []
    return db_chat


@router.post("/", response_model=Chat, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_create: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создаёт новый чат.
    
    Поле `creator_id` автоматически заполняется из токена.
    """
    chat_data = chat_create.dict()
    new_chat = await crud_chat.create(db, chat_data, current_user)
    new_chat.participant_ids = [user.id for user in new_chat.participants] if new_chat.participants else []
    return new_chat


@router.patch("/{chat_id}", response_model=Chat)
async def update_chat(
    chat_id: int,
    chat_update: ChatUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновляет данные чата.
    
    Обновление доступно только для создателя чата.
    """
    db_chat = await crud_chat.get(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    if db_chat.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this chat")
    
    updated_chat = await crud_chat.update(db, db_chat, chat_update.dict(exclude_unset=True))
    updated_chat.participant_ids = [user.id for user in updated_chat.participants] if updated_chat.participants else []
    return updated_chat



@router.delete("/{chat_id}", response_model=Chat)
async def delete_chat(
    chat_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удаляет чат.
    
    Удаление доступно только для создателя чата.
    """
    db_chat = await crud_chat.get(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    if db_chat.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this chat")
    
    deleted_chat = await crud_chat.remove(db, db_chat)
    deleted_chat.participant_ids = [user.id for user in deleted_chat.participants] if deleted_chat.participants else []
    return deleted_chat
