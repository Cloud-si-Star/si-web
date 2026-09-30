from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MenuCreate(BaseModel):
    """新增菜单请求体。"""

    parent_id: int = Field(default=0, ge=0, description="父菜单ID，0表示顶级菜单")
    label: str = Field(min_length=1, max_length=50)
    icon: str = Field(min_length=1, max_length=50)
    path: str = Field(min_length=1, max_length=100)
    component: str = Field(min_length=1, max_length=100)
    sort_order: int = Field(default=0, ge=0)
    visible: Literal[0, 1] = 1
    menu_type: Literal[1, 2] = Field(description="1工作台，2可视化")


class MenuVisibilityUpdate(BaseModel):
    """菜单启用/关闭请求体。"""

    visible: Literal[0, 1]


class MenuResponse(BaseModel):
    """菜单记录响应，字段名与 sys_menu 数据库列保持一致。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int
    label: str
    icon: str
    path: str
    component: str
    sort_order: int
    visible: Literal[0, 1]
    menu_type: int
    created_at: datetime
    updated_at: datetime


class MenuTreeResponse(MenuResponse):
    """树形菜单节点；子节点继续使用相同字段结构。"""

    children: list["MenuTreeResponse"] = Field(default_factory=list)