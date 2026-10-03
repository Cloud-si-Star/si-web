"""
chat_service.py
作用：会话和消息的业务逻辑，全部用 ORM 操作
位置：your_project/service/chat_service.py
说明：所有函数接收 db（Session）作为第一个参数，由 router 层注入
"""
import re
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.chat_entity import ChatConversation, ChatMessage

# 当前写死的用户ID，以后接登录改这里
DEFAULT_USER_ID = 8


# ==================== 会话表 ====================

def create_conversation(db: Session, title: str = "新对话") -> int:
    """
    新建会话
    对应 SQL: INSERT INTO chat_conversation (user_id, title) VALUES (?, ?)
    """
    obj = ChatConversation(user_id=DEFAULT_USER_ID, title=title)
    db.add(obj)  # 加入待提交队列
    db.commit()  # 真正执行 INSERT
    db.refresh(obj)  # 回读，拿到自增 id 和默认值
    return obj.id


def list_conversations(db: Session) -> List[dict]:
    """
    左边栏列表，按最近更新倒序
    对应 SQL: SELECT ... WHERE user_id=? ORDER BY updated_at DESC
    """
    rows = (
        db.query(ChatConversation)
        .filter(ChatConversation.user_id == DEFAULT_USER_ID)
        .order_by(ChatConversation.updated_at.desc())
        .all()
    )
    # ORM 对象转 dict，方便 Pydantic 序列化
    return [
        {
            "id": r.id,
            "title": r.title,
            "last_message": r.last_message,
            "message_count": r.message_count,
        }
        for r in rows
    ]


def get_conversation(db: Session, conversation_id: int) -> Optional[ChatConversation]:
    """按 id 查会话，返回 ORM 对象或 None"""
    return (
        db.query(ChatConversation)
        .filter(ChatConversation.id == conversation_id)
        .first()
    )


def update_conversation_after_message(db: Session, conversation_id: int, last_message: str):
    """
    每存一条消息后调用：更新 last_message 和 message_count
    updated_at 由 ORM 的 onupdate 自动更新，不用手动写
    """
    conv = get_conversation(db, conversation_id)
    if conv:
        conv.last_message = last_message[:255]  # 防超长
        conv.message_count = (conv.message_count or 0) + 1
        # 改了对象属性后 commit，ORM 自动生成 UPDATE
        db.commit()


def update_conversation_title(db: Session, conversation_id: int, title: str):
    """改标题（可选功能）"""
    conv = get_conversation(db, conversation_id)
    if conv:
        conv.title = title[:64]
        db.commit()


def delete_conversation(db: Session, conversation_id: int):
    """
    删除会话及其所有消息
    先删消息，再删会话（表间没写外键级联，手动删）
    """
    db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).delete()
    db.query(ChatConversation).filter(
        ChatConversation.id == conversation_id
    ).delete()
    db.commit()


# ==================== 消息表 ====================

def save_message(db: Session, conversation_id: int, role: str, content: str) -> int:
    """
    存一条消息，返回消息 id
    对应 SQL: INSERT INTO chat_message (...) VALUES (...)
    """
    obj = ChatMessage(conversation_id=conversation_id, role=role, content=content)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj.id


def list_messages(db: Session, conversation_id: int) -> List[dict]:
    """
    查某会话全部历史消息，按 id 升序
    对应 SQL: SELECT ... WHERE conversation_id=? ORDER BY id ASC
    """
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )
    return [
        {"id": r.id, "role": r.role, "content": r.content}
        for r in rows
    ]


def is_first_message(db: Session, conversation_id: int) -> bool:
    """判断该会话当前是否还没有消息（即这是第一条）"""
    count = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).count()
    return count == 0


def generate_title_from_message(content: str, max_len: int = 9) -> str:
    """
    从用户第一条消息生成标题：
    - 去掉换行和多余空格
    - 截取前 max_len 个字
    - 超长加省略号
    """
    clean = re.sub(r'\s+', ' ', content).strip()
    if not clean:
        return "新对话"
    if len(clean) <= max_len:
        return clean
    return clean[:max_len] + "..."
