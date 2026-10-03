from app.schemas.base import CamelModel

from typing import List, Optional


# ---------- 消息 ----------
class MessageItem(CamelModel):
    role: str
    content: str


class ChatRequest(CamelModel):
    # 请求体比之前多一个conversation_id
    conversation_id: int
    messages: List[MessageItem]


class MessageResponse(CamelModel):
    id: int
    role: str
    content: str


# ---------- 会话 ----------
class NewConversationResponse(CamelModel):
    # 左边一栏
    conversation_id: int
    title: str


class ConversationItem(CamelModel):
    # 左边一栏
    id: int
    title: str
    last_message: Optional[str] = None
    message_count: int = 0


class ConversationListResponse(CamelModel):
    list: List[ConversationItem]
