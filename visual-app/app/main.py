from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import data
from app.api.v2 import mock
from app.utils.exceptions import register_exception_handlers

app = FastAPI(title=settings.app_name, version=settings.version)

# 允许前端跨域访问（开发环境放开，生产请收紧 allow_origins）
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


@app.get("/")
def health():
    return {"code": 0, "message": "ok", "data": {"service": settings.app_name}}
