from sqlalchemy import BigInteger, Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

"""
chat_entity.py
作用：ORM 模型类，把 chat_conversation / chat_message 两张表映射成 Python 类
位置：your_project/model/chat_entity.py
说明：继承 database.Base，SQLAlchemy 靠它知道类与表的对应关系
"""


class ChatConversation(Base):
    # 对应表名
    __tablename__ = "chat_conversation"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="会话ID")
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    title = Column(String(64), nullable=False, default="新对话", comment="会话标题")
    last_message = Column(String(255), nullable=True, comment="最后一条消息摘要")
    message_count = Column(Integer, nullable=False, default=0, comment="消息数量")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="信息ID")
    conversation_id = Column(BigInteger, nullable=False, index=True, comment="所属会话ID")
    role = Column(String(20), nullable=False, comment="角色: user/assistant/system")
    content = Column(Text, nullable=False, comment="消息内容")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
