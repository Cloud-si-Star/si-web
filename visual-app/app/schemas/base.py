# app/schemas/base.py
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """对外自动转驼峰的基类：内部下划线，前端传/收驼峰"""
    model_config = ConfigDict(
        alias_generator=to_camel,  # 下划线 → 驼峰
        populate_by_name=True,  # 下划线名也接受
        from_attributes=True,  # 支持从 ORM 对象转换
    )
