from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat_model import (
    ChatMessageCreate,
    ConversationItem,
    MessageResponse,
    NewConversationResponse,
)
from app.schemas.response import ResponseModel, success
from app.services import chat_service
from app.services.chat_provider import get_chat_client

conversations_router = APIRouter(prefix="/conversations", tags=["conversations"])
mock_router = APIRouter(prefix="/chat", tags=["chat"])


@conversations_router.post("", response_model=ResponseModel[NewConversationResponse], status_code=201)
def create_conversation(db: Session = Depends(get_db)):
    """Create a conversation."""
    title = "新对话"
    conversation_id = chat_service.create_conversation(db, title=title)
    return success(data={"conversation_id": conversation_id, "title": title})


@conversations_router.get("", response_model=ResponseModel[list[ConversationItem]])
def list_conversations(db: Session = Depends(get_db)):
    """List conversations ordered by most recently updated."""
    return success(data=chat_service.list_conversations(db))


@conversations_router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Read the message history for a conversation."""
    if not chat_service.get_conversation(db, conversation_id):
        raise HTTPException(status_code=404, detail="会话不存在")
    return chat_service.list_messages(db, conversation_id)


@conversations_router.post("/{conversation_id}/messages")
async def create_conversation_message(
    conversation_id: int,
    request: ChatMessageCreate,
    db: Session = Depends(get_db),
):
    """Store the user message and stream the assistant reply using SSE."""
    if not chat_service.get_conversation(db, conversation_id):
        raise HTTPException(status_code=404, detail="会话不存在")

    last_message = request.messages[-1]
    if last_message.role != "user":
        raise HTTPException(status_code=422, detail="最后一条消息必须来自 user")

    if chat_service.is_first_message(db, conversation_id):
        title = chat_service.generate_title_from_message(last_message.content)
        chat_service.update_conversation_title(db, conversation_id, title)

    chat_service.save_message(db, conversation_id, "user", last_message.content)
    chat_service.update_conversation_after_message(db, conversation_id, last_message.content)

    sdk_messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    def event_generator():
        buffer = ""
        try:
            stream = get_chat_client().chat.completions.create(
                model="ernie-4.5-turbo-32k",
                messages=sdk_messages,
                stream=True,
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    buffer += content
                    yield f"data: {content}\n\n"

            if buffer:
                chat_service.save_message(db, conversation_id, "assistant", buffer)
                chat_service.update_conversation_after_message(db, conversation_id, buffer)

            yield "data: [DONE]\n\n"
        except Exception as error:
            if buffer:
                chat_service.save_message(db, conversation_id, "assistant", buffer)
                chat_service.update_conversation_after_message(db, conversation_id, buffer)
            yield f"data: [ERROR] {error}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@conversations_router.delete("/{conversation_id}", response_model=ResponseModel[None])
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Delete a conversation and its messages."""
    if not chat_service.get_conversation(db, conversation_id):
        raise HTTPException(status_code=404, detail="会话不存在")
    chat_service.delete_conversation(db, conversation_id)
    return success(message="删除成功")


@mock_router.post("/mock")
async def mock_chat(request: ChatMessageCreate):
    """Stream a model reply without saving a conversation."""
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    def event_generator():
        try:
            stream = get_chat_client().chat.completions.create(
                model="ernie-4.5-turbo-32k",
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield f"data: {content}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as error:
            yield f"data: [ERROR] {error}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
