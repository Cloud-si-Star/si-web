from datetime import date
from pydantic import BaseModel, Field

from app.schemas.base import CamelModel


class AiInfoQuery(BaseModel):
    """列表查询条件"""
    ai_name: str | None = Field(None, description="AI 名称，模糊匹配")
    ai_status: str | None = Field(None, description="AI 状态")
    ai_date: date | None = Field(None, description="创建日期，格式 YYYY-MM-DD")

    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, alias="pageSize", description="每页条数")

    model_config = {"from_attributes": True}


class AiInfoItem(BaseModel):
    """单条 AI 信息"""
    id: int
    ai_id: int
    ai_name: str
    ai_use: int | None = None
    ai_status: str | None = None
    create_time: str | None = None
    remark: str | None = None

    model_config = {"from_attributes": True}


class AiInfoPage(BaseModel):
    """分页结果"""
    list: list[AiInfoItem]
    total: int
    page: int
    page_size: int


class AiInfoUpdate(CamelModel):
    """PATCH 部分更新：所有字段可选"""
    ai_id: int
    ai_name: str | None = None
    remark: str | None = None
    ai_use: int | None = None
    ai_status: str | None = None
