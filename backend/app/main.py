# backend/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.app.routes import database_routes
from backend.app.services.sql_server_service import DatabaseManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理器。
    """
    # 启动时的事件
    print("Application startup: Initializing resources...")
    yield
    # 关闭时的事件
    print("Application shutdown: Releasing resources...")
    DatabaseManager.close_connection()

# 创建 FastAPI 实例
app = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(database_routes.router, prefix="/api/v1/database", tags=["Database"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI Application!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

