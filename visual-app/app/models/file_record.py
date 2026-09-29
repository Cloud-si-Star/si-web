from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base


class FileRecord(Base):
    __tablename__ = "file_record"
    __table_args__ = {"comment": "文件上传记录表"}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    file_name = Column(String(255), nullable=False, comment="原始文件名")
    file_type = Column(String(50), nullable=False, comment="文件类型/扩展名")
    file_path = Column(String(500), nullable=False, comment="文件存储路径")
    file_size = Column(Integer, nullable=False, comment="文件大小（字节）")
    upload_user = Column(String(100), nullable=True, comment="上传用户")
    upload_time = Column(DateTime, nullable=False, default=datetime.now, comment="上传时间")
    remark = Column(Text, nullable=True, comment="备注")
