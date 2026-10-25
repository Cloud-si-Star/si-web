import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI


@lru_cache(maxsize=1)
def get_chat_client() -> OpenAI:
    """Create the remote chat client on first use, not during API import."""
    load_dotenv()
    api_key = os.getenv("ERNIE_API_KEY")
    if not api_key:
        raise RuntimeError("请在 .env 配置 ERNIE_API_KEY")

    return OpenAI(
        api_key=api_key,
        base_url="https://qianfan.baidubce.com/v2",
    )
