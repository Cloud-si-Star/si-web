from typing import Literal

from pydantic import Field

from app.schemas.base import CamelModel


class ChatMessageItem(CamelModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatMessageCreate(CamelModel):
    messages: list[ChatMessageItem] = Field(min_length=1)


class MessageResponse(CamelModel):
    id: int
    role: str
    content: str


class NewConversationResponse(CamelModel):
    conversation_id: int
    title: str


class ConversationItem(CamelModel):
    id: int
    title: str
    last_message: str | None = None
    message_count: int = 0


class ConversationListResponse(CamelModel):
    list: list[ConversationItem]
