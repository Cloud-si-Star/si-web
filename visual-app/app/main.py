from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.ai_usage import router as ai_usage_router
from app.api.v1.chat import conversations_router, mock_router
from app.api.v1.files import router as files_router
from app.api.v1.menus import router as menus_router
from app.api.v1.sales import router as sales_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logger import logger
from app.utils.exceptions import register_exception_handlers
import app.models

Base.metadata.create_all(bind=engine)

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

# Register versioned resource routes.
API_V1_PREFIX = "/api/v1"
app.include_router(files_router, prefix=API_V1_PREFIX)
app.include_router(ai_usage_router, prefix=API_V1_PREFIX)
app.include_router(menus_router, prefix=API_V1_PREFIX)
app.include_router(conversations_router, prefix=API_V1_PREFIX)
app.include_router(mock_router, prefix=API_V1_PREFIX)
app.include_router(sales_router, prefix=API_V1_PREFIX)


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
