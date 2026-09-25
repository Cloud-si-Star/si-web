from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from app.schemas.response import ResponseModel
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 读取环境变量
ERNIE_API_KEY = os.getenv("ERNIE_API_KEY")

# 校验，如果没读到直接抛出错误，防止空密钥
if not ERNIE_API_KEY:
    raise Exception("请在.env配置 ERNIE_API_KEY")

router = APIRouter(prefix="/mock", tags=["mock"])



# 启动前执行：export QIANFAN_API_KEY="your_key_here"
client = OpenAI(
    api_key=ERNIE_API_KEY,
    base_url="https://qianfan.baidubce.com/v2",  # 千帆 v2 接口地址 [citation:1]
)

class ChatRequest(BaseModel):
    messages: list

@router.post("/chat", response_model=ResponseModel)
async def chat(request: ChatRequest):
    """流式对话接口，以 SSE 格式返回"""

    def event_generator():
        try:
            stream = client.chat.completions.create(
                model="ernie-4.5-turbo-32k",  # 你的模型
                messages=request.messages,
                stream=True,
            )


            for chunk in stream:
                delta = chunk.choices[0].delta
                content = delta.content
                # 千帆的 ernie 系列可能不返回 reasoning_content，直接取 content 即可 [citation:1]
                if content:
                    yield f"data: {content}\n\n"

            yield "data: [DONE]\n\n"
        except Exception as e:
            # 走这里 报错了
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 防止 nginx 缓冲流式响应
        },
    )