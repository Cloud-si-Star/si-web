import logging
from enum import IntEnum

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import logger

__all__ = [
    "BizException",
    "ErrorCode",
    "register_exception_handlers",
]


class ErrorCode(IntEnum):
    """业务错误码枚举"""
    SUCCESS = 0
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    VALIDATION_ERROR = 422
    INTERNAL_ERROR = 500


class BizException(Exception):
    """
    业务异常基类

    在业务代码中直接 raise 此异常，会返回统一格式的响应
    """

    def __init__(self, message: str, code: int = -1, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "data": self.details,
        }


class ResourceNotFoundException(BizException):
    """资源不存在异常"""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource}不存在: {identifier}",
            code=ErrorCode.NOT_FOUND,
        )


class ValidationException(BizException):
    """参数校验异常"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            details=details,
        )


class UnauthorizedException(BizException):
    """未授权异常"""

    def __init__(self, message: str = "未授权访问"):
        super().__init__(message=message, code=ErrorCode.UNAUTHORIZED)


class ForbiddenException(BizException):
    """禁止访问异常"""

    def __init__(self, message: str = "禁止访问"):
        super().__init__(message=message, code=ErrorCode.FORBIDDEN)


def register_exception_handlers(app):
    """注册全局异常处理器"""

    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        logger.warning(
            f"业务异常: {exc.message}, path={request.url.path}, details={exc.details}"
        )
        return JSONResponse(
            status_code=200,
            content=exc.to_dict(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        logger.warning(f"参数校验失败: {errors}, path={request.url.path}")
        return JSONResponse(
            status_code=200,
            content={
                "code": ErrorCode.VALIDATION_ERROR,
                "message": "参数校验失败",
                "data": errors,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(
            f"服务器内部错误: {str(exc)}, path={request.url.path}",
            exc_info=True
        )
        return JSONResponse(
            status_code=200,
            content={
                "code": ErrorCode.INTERNAL_ERROR,
                "message": f"服务器内部错误: {str(exc)}",
                "data": None,
            },
        )
