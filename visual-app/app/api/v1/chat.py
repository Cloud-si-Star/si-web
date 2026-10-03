"""
conversation_router.py
作用：会话管理接口（新建/列表/历史消息/删除）
位置：your_project/router/conversation_router.py
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.response import ResponseModel, success
from app.core.database import get_db
from app.schemas.chat_model import (
    NewConversationResponse,
    ConversationListResponse,
    MessageResponse,
    ConversationItem,
)
from app.services import chat_service

router = APIRouter(prefix="/conversation", tags=["会话管理"])


@router.post("/new", response_model=ResponseModel[NewConversationResponse])
async def new_conversation(db: Session = Depends(get_db)):
    """新建会话，前端点'新对话'时调用"""
    cid = chat_service.create_conversation(db, title="新对话")
    return success(data={"conversation_id": cid, "title": "新对话"})


@router.get("/list", response_model=ResponseModel[list[ConversationItem]])
async def conversation_list(db: Session = Depends(get_db)):
    """左边栏会话列表"""
    rows = chat_service.list_conversations(db)
    return success(data=rows)


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
async def conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    """加载某会话的历史消息"""
    conv = chat_service.get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="会话不存在")
    return chat_service.list_messages(db, conversation_id)


@router.delete("/{conversation_id}")
async def remove_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """删除会话及其消息"""
    chat_service.delete_conversation(db, conversation_id)
    return {"message": "删除成功"}
