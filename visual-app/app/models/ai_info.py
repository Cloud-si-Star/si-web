from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class AiInfo(Base):
    __tablename__ = "ai_info"
    __table_args__ = {"comment": "AI 信息表"}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    ai_id = Column(Integer, unique=True, nullable=False, comment="AI 编号")
    ai_name = Column(String(50), nullable=False, comment="AI 名称")
    ai_use = Column(Integer, default=0, comment="使用次数")
    ai_status = Column(String(20), comment="状态文本，如 offline")
    ai_status_code = Column(Integer, comment="状态码，0=离线 1=在线")
    create_time = Column(DateTime, comment="创建时间")
    remark = Column(String(255), comment="备注")
