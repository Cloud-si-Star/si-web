from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.dialects.mysql import INTEGER

from app.core.database import Base


class Menu(Base):
    """系统菜单，对应 sys_menu 表。"""

    __tablename__ = "sys_menu"
    __table_args__ = {"comment": "系统菜单表"}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment="菜单ID")
    parent_id = Column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"), comment="父菜单ID")
    label = Column(String(50), nullable=False, comment="菜单名称")
    icon = Column(String(50), nullable=False, comment="菜单图标")
    path = Column(String(100), nullable=False, comment="菜单路径")
    component = Column(String(100), nullable=False, comment="菜单组件")
    sort_order = Column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"), comment="排序")
    visible = Column(Integer, nullable=False, default=1, server_default=text("1"), comment="是否可见（0否，1是）")
    menu_type = Column(Integer, nullable=False, default=0, server_default=text("0"), comment="菜单类型（1工作台，2可视化）")
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        comment="更新时间",
    )