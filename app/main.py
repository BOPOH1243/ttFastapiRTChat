# File: app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from app.api import websocket, history, auth, chat
from app.core.database import engine, Base

app = FastAPI(title="Real-Time Chat API")

# Подключаем роутеры для Auth, Chat, History и WebSocket
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(history.router)
app.include_router(websocket.router)


templates = Jinja2Templates(directory="app/templates")

# Роут для отображения chat.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "chat.html", {"request": request}
    )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Real-Time Chat API",
        version="1.0.0",
        description="Документация для Real-Time Chat API с JWT авторизацией",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Добавляем схему безопасности для всех эндпоинтов, требующих авторизации
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Запуск приложения через Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
