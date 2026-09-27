from app.core.database import Base, engine
from app.models.ai_info import AiInfo  # noqa: F401  必须导入，才会注册到 Base


def create_table():
    """建 ai_info 表（已存在则跳过）"""
    Base.metadata.create_all(bind=engine)
    print("ai_info 表已就绪")


if __name__ == "__main__":
    create_table()
