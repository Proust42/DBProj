# backend/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.app.services.sql_server_service import SQLServerDatabaseManager
from backend.app.routes.sql_server_routes import router as sql_server_router
from backend.app.routes.mongo_routes import router as mongo_router

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
    SQLServerDatabaseManager.close_connection()

# 创建 FastAPI 实例
app = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(sql_server_router, prefix="/api/v1/sql_server_database", tags=["SQLServerDatabase"])
app.include_router(mongo_router, prefix="/api/v1/mongo_database", tags=["MongoDB"])



@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Datebase Application!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

