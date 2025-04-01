# File: app/main.py
from fastapi import FastAPI
from app.api import websocket, history
from app.core.database import engine, Base

app = FastAPI(title="Real-Time Chat API")

# Include routers for WebSocket and REST API
app.include_router(websocket.router, prefix="/api")
app.include_router(history.router, prefix="/api")

# Create all tables at startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Real-Time Chat API is running"}

# Entry point for running the application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
