"""
ETL 业务服务层。
设计纪律：
1. 不 commit / rollback —— 事务边界交给路由层
2. 不抛 HTTPException —— 只抛业务异常，路由层翻译成状态码
3. 每个函数可被其他 service 复用
"""
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.logger import logger  # 用你已封装的 logger


class EtlError(Exception):
    """业务异常，路由层捕获后转 500"""
    pass


def validate_bizdate(bizdate: str) -> str:
    """校验日期格式，非法直接抛 ValueError"""
    try:
        datetime.strptime(bizdate, "%Y%m%d")
    except ValueError:
        # 理论上 Pydantic 已拦，这里兜底（service 可能被内部调用）
        raise ValueError(f"bizdate 格式错误，应为 YYYYMMDD: {bizdate}")
    return bizdate


def run_dws_sales_daily(db: Session, bizdate: str) -> int:
    """
    执行 dws_sales_daily 的日汇总 ETL。
    幂等：先 DELETE 目标分区，再 INSERT。
    事务：不在此 commit，由调用方统一提交。
    返回：写入行数。
    """
    validate_bizdate(bizdate)
    logger.info(f"[ETL] 开始 dws_sales_daily bizdate={bizdate}")

    try:
        # 步骤 1：幂等保障 —— 清空目标分区
        # 用 text() 写原生 SQL，因为这是批处理聚合，ORM 反而累赘
        deleted = db.execute(
            text("DELETE FROM dws_sales_daily WHERE dt = :dt"),
            {"dt": bizdate},
        ).rowcount
        logger.info(f"[ETL] 清理旧数据 bizdate={bizdate}, rows={deleted}")

        # 步骤 2：聚合写入
        # 注意 :dt 出现两次：一次是 SELECT 的常量列，一次是 WHERE 过滤
        inserted = db.execute(
            text("""
                INSERT INTO dws_sales_daily
                    (dt, category, region, order_cnt, total_qty, total_amount, total_profit)
                SELECT
                    :dt                    AS dt,
                    p.category,
                    r.region,
                    COUNT(*)               AS order_cnt,
                    SUM(f.quantity)        AS total_qty,
                    SUM(f.amount)          AS total_amount,
                    SUM(f.amount - f.cost) AS total_profit
                FROM fact_sales f
                JOIN dim_product p ON f.product_id = p.product_id
                JOIN dim_region  r ON f.region_id  = r.region_id
                WHERE f.dt = :dt
                GROUP BY p.category, r.region
            """),
            {"dt": bizdate},
        ).rowcount
        logger.info(f"[ETL] 写入新数据 bizdate={bizdate}, rows={inserted}")

        # 步骤 3：空结果告警（不抛异常，业务上允许某天无数据）
        if inserted == 0:
            logger.warning(f"[ETL] bizdate={bizdate} 无数据写入，请确认源表")

        return inserted

    except ValueError:
        raise  # 校验类异常直接上抛，路由层转 422/400
    except Exception as e:
        # 业务执行异常，包装后上抛，路由层转 500
        logger.error(f"[ETL] 执行失败 bizdate={bizdate}: {e}", exc_info=True)
        raise EtlError(f"dws_sales_daily ETL 失败: {e}") from e
