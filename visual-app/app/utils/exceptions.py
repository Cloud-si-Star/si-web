from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class BizException(Exception):
    """业务异常，接口里可直接 raise"""
    def __init__(self, message: str, code: int = -1):
        self.code = code
        self.message = message


def register_exception_handlers(app):
    """把全局异常处理挂到 app 上，保证异常也返回统一结构"""

    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        return JSONResponse(
            status_code=200,
            content={"code": exc.code, "message": exc.message, "data": None},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=200,
            content={"code": 422, "message": "参数校验失败", "data": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=200,
            content={"code": 500, "message": f"服务器内部错误: {exc}", "data": None},
        )
