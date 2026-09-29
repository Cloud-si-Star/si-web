from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """
    统一响应体结构

    Attributes:
        code: 状态码，0表示成功
        message: 响应消息
        data: 响应数据
    """
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


def success(data: Any = None, message: str = "success") -> ResponseModel:
    """
    成功响应

    Args:
        data: 响应数据
        message: 响应消息

    Returns:
        ResponseModel 实例
    """
    return ResponseModel(code=0, message=message, data=data)


def error(
        code: int = -1,
        message: str = "error",
        data: Any = None
) -> ResponseModel:
    """
    失败响应

    Args:
        code: 错误码
        message: 错误消息
        data: 错误详情数据

    Returns:
        ResponseModel 实例
    """
    return ResponseModel(code=code, message=message, data=data)


def paginated(
        items: list,
        total: int,
        page: int,
        page_size: int,
        message: str = "success"
) -> ResponseModel:
    """
    分页响应

    Args:
        items: 当前页数据列表
        total: 总记录数
        page: 当前页码
        page_size: 每页条数
        message: 响应消息

    Returns:
        ResponseModel 实例，包含分页信息
    """
    return ResponseModel(
        code=0,
        message=message,
        data={
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    )
