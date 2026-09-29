from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import logger
from app.api.v1 import data
from app.api.v2 import mock
from app.utils.exceptions import register_exception_handlers

# 应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Visual App API Service",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理
register_exception_handlers(app)

# 注册路由
app.include_router(data.router, prefix="/api/v1")
app.include_router(mock.router, prefix="/api/v2")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"{settings.app_name} v{settings.version} 启动成功")


@app.get("/")
async def health_check():
    """健康检查接口"""
    return {
        "code": 0,
        "message": "ok",
        "data": {
            "service": settings.app_name,
            "version": settings.version,
            "status": "running",
        }
    }


@app.get("/health")
async def health():
    """详细健康检查"""
    return {
        "code": 0,
        "message": "ok",
        "data": {
            "service": settings.app_name,
            "version": settings.version,
            "status": "healthy",
        }
    }
