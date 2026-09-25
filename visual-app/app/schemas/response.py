from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """统一响应体结构：code / message / data"""
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


def success(data: Any = None, message: str = "success") -> ResponseModel:
    """成功响应"""
    return ResponseModel(code=0, message=message, data=data)


def error(code: int = -1, message: str = "error", data: Any = None) -> ResponseModel:
    """失败响应"""
    return ResponseModel(code=code, message=message, data=data)
