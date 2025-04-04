import jwt
from fastapi import WebSocket, HTTPException, status
from typing import Dict
from app.core.security import SECRET_KEY, ALGORITHM

class ConnectionManager:
    """
    Менеджер WebSocket-соединений.
    
    Сохраняет активные соединения в виде словаря, где ключ — ID пользователя,
    а значение — WebSocket-соединение.
    """
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> int:
        """
        Обрабатывает новое соединение:
          - Извлекает JWT из query-параметра 'token'.
          - Валидирует токен и извлекает user_id.
          - Принимает соединение и сохраняет его в списке активных.
        
        :param websocket: Объект WebSocket.
        :return: Идентификатор пользователя (user_id).
        :raises HTTPException: Если токен отсутствует или недействителен.
        """
        token = websocket.query_params.get("token")
        if not token:
            # Закрываем соединение, если токен не предоставлен
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise HTTPException(
                status_code=status.WS_1008_POLICY_VIOLATION, 
                detail="Token not provided"
            )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                raise HTTPException(
                    status_code=status.WS_1008_POLICY_VIOLATION, 
                    detail="Invalid token: missing subject"
                )
            user_id = int(user_id)
        except jwt.PyJWTError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise HTTPException(
                status_code=status.WS_1008_POLICY_VIOLATION, 
                detail="Token validation error"
            )
        
        # Принять соединение и сохранить его
        await websocket.accept()
        self.active_connections[user_id] = websocket
        return user_id

    def disconnect(self, user_id: int):
        """
        Удаляет соединение из списка активных при отключении пользователя.
        
        :param user_id: Идентификатор пользователя.
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_notification(self, user_id: int, message: dict):
        
        """
        Отправляет уведомление (JSON-сообщение) пользователю с заданным ID.
        
        :param user_id: Идентификатор пользователя.
        :param message: Словарь с данными уведомления.
        """
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)
        print(f'уведомление отправлено {user_id}')

manager = ConnectionManager()