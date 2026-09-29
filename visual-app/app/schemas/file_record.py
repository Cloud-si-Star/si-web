from datetime import date, datetime
from typing import Optional

from pydantic import Field

from app.schemas.base import CamelModel


class FileRecordQuery(CamelModel):
    """文件记录查询条件"""
    file_name: Optional[str] = Field(None, description="文件名，模糊匹配")
    file_type: Optional[str] = Field(None, description="文件类型")
    upload_user: Optional[str] = Field(None, description="上传用户")
    start_date: Optional[date] = Field(None, description="上传开始日期")
    end_date: Optional[date] = Field(None, description="上传结束日期")

    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, alias="pageSize", description="每页条数")


class FileRecordItem(CamelModel):
    """文件记录详情"""
    id: int
    file_name: str
    file_type: str
    file_path: str
    file_size: int
    upload_user: Optional[str] = None
    upload_time: str
    remark: Optional[str] = None

    model_config = {"from_attributes": True}


class FileRecordPage(CamelModel):
    """分页结果"""
    list: list[FileRecordItem]
    total: int
    page: int
    page_size: int


class FileRecordCreate(CamelModel):
    """创建文件记录"""
    file_name: str = Field(..., description="原始文件名")
    file_type: str = Field(..., description="文件类型/扩展名")
    file_path: str = Field(..., description="文件存储路径")
    file_size: int = Field(..., description="文件大小（字节）")
    upload_user: Optional[str] = Field(None, description="上传用户")
    remark: Optional[str] = Field(None, description="备注")
