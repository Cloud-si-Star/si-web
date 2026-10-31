from pydantic import Field
from app.schemas.base import CamelModel


class BizResponse(CamelModel):
    """
    定义跑批数据响应体
    1、bizDate  什么时间
    2、insertTotal 插入数量
    """
    bizDate: str
    insertTotal: int = 0
    dropCount: int = 0
    actConut: int = 0


class MonthlyBizDayResponse(CamelModel):
    biz_date: str
    insert_total: int = 0
    drop_count: int = 0


class MonthlyBizResponse(CamelModel):
    biz_month: str
    start_date: str
    end_date: str
    total_days: int
    insert_total: int = 0
    drop_count: int = 0
    results: list[MonthlyBizDayResponse]
