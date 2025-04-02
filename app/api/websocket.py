# File: app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.security import verify_token
from app.services.chat_service import manager

router = APIRouter(tags=["websocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    payload = verify_token(token)
    if payload is None:
        await websocket.close(code=1008)
        return
    user_id = int(payload.get("sub"))
    await manager.connect(user_id, websocket)
    try:
        while True:
            # Ожидаем сообщения (например, пинги) от клиента, но основная цель – уведомления с сервера
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
