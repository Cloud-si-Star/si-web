"""
chat_router.py
作用：流式对话接口，边返回给前端、边存库
位置：your_project/router/chat_router.py

⚠️ 把 your_qianfan_client 换成你实际初始化 client 的导入
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat_model import ChatRequest
from app.services import chat_service

# ⚠️ 换成你实际 client 的位置（原来 /chat 里用的那个）
from app.api.v2.use_chat import client

router = APIRouter(tags=["对话"])


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    流式对话接口（SSE）

    改动点：
    1. 请求进来，先把用户最新消息存库
    2. 调模型，流式返回给前端
    3. 同时累积模型回复
    4. 流结束时，把完整回复存库
    5. 更新会话 last_message / message_count
    """
    conversation_id = request.conversation_id

    # ---------- 第1步：存用户消息 ----------
    last_msg = request.messages[-1]
    if last_msg.role == "user":
        # 先判断是不是该会话的第一条？
        is_first = chat_service.is_first_message(db, conversation_id)

        # 存用户消息
        chat_service.save_message(db, conversation_id, "user", last_msg.content)
        chat_service.update_conversation_after_message(db, conversation_id, last_msg.content)

        if is_first:
            new_title = chat_service.generate_title_from_message(last_msg.content)
            chat_service.update_conversation_title(db, conversation_id, new_title)

    # ---------- 第2步：转 SDK 格式 ----------
    sdk_messages = [{"role": m.role, "content": m.content} for m in request.messages]

    def event_generator():
        buffer = ""  # 累积模型完整回复
        try:
            stream = client.chat.completions.create(
                model="ernie-4.5-turbo-32k",
                messages=sdk_messages,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                content = delta.content
                if content:
                    buffer += content
                    yield f"data: {content}\n\n"

            # ---------- 第3步：流结束，存模型回复 ----------
            if buffer:
                chat_service.save_message(db, conversation_id, "assistant", buffer)
                chat_service.update_conversation_after_message(db, conversation_id, buffer)

            yield "data: [DONE]\n\n"

        except Exception as e:
            # 出错时，已收到的部分也存下来
            if buffer:
                chat_service.save_message(db, conversation_id, "assistant", buffer)
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
