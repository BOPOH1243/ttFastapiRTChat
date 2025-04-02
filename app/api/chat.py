# File: app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.chat import ChatBase, ChatResponse
from app.schemas.message import MessageCreate, MessageResponse
from app.crud.chat import create_chat, get_user_chats
from app.crud.message import create_message, get_messages
from app.crud.group import remove_user_from_group

router = APIRouter(prefix="/chat", tags=["chat"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> int:
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.post("/", response_model=ChatResponse)
async def create_new_chat(chat: ChatBase, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_chat = await create_chat(db, chat)
    return new_chat

@router.get("/my", response_model=list[ChatResponse])
async def get_my_chats(current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chats = await get_user_chats(db, current_user)
    return chats

@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
async def get_chat_messages(chat_id: int, limit: int = 50, offset: int = 0, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    messages = await get_messages(db, chat_id, limit, offset)
    return messages

@router.post("/{chat_id}/message", response_model=MessageResponse)
async def send_message(chat_id: int, message: MessageCreate, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if message.sender_id != current_user:
        raise HTTPException(status_code=403, detail="Sender mismatch")
    created_message = await create_message(db, message)
    if not created_message:
        raise HTTPException(status_code=400, detail="Duplicate message")
    return created_message

@router.delete("/{chat_id}/user/{user_id}")
async def remove_user(chat_id: int, user_id: int, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await remove_user_from_group(db, chat_id, user_id)
    if not result:
        raise HTTPException(status_code=400, detail="Unable to remove user")
    return {"detail": "User removed from chat"}
