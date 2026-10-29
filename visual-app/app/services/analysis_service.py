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


'fact_sales->ods_sales->dwd_sales_detail->dws_sales_daily,dws_sales_daily_category,dws_sales_monthly_region'
'业务数据      贴源层      数据仓库明细层       数据仓库汇总层'


def run_ods_sales(db: Session, bizdate: str) -> int:
    """
    ----------
    db 数据库会话
    bizdate 跑批数据时间
    从业务层获取数据 建立数据贴源层 隔离业务库
    Returns 插入多少条
    -------
    """
    validate_bizdate(bizdate)
    logger.info(f"[ETL] 开始 ods_sales bizdate={bizdate}")
    delete_sql = text("DELETE FROM ods_sales WHERE dt= :bizdate")

    insert_sql = text("""
        INSERT INTO ods_sales (id, date_id, product_id, region_id, quantity, amount, cost, dt, src_table)
        SELECT 
            f.id, f.date_id, f.product_id, f.region_id,
            f.quantity, f.amount, f.cost,
            f.dt,
            'fact_sales' as src_table
        FROM fact_sales f 
        WHERE f.dt=:bizdate
    """)
    try:

        db.execute(delete_sql, {"bizdate": bizdate})
        inserted = db.execute(insert_sql, {"bizdate": bizdate}).rowcount
        db.commit()
        logger.info(f"[ods_sales] bizdate={bizdate} 抽{inserted}行")
        return inserted
    except Exception:

        db.rollback()
        logger.exception(f"[ods_sales] bizdate={bizdate} 失败已回滚")
        raise


def run_dwd_sales_detail(db: Session, bizdate: str) -> dict:
    """
    ----------
    db 数据库会话
    bizdate 跑批数据时间
    从贴源层获取数据仓库明细层
    Returns 插入多少条
    -------
    """
    delete_sql = text("DELETE FROM dwd_sales_detail WHERE dt = :bizdate")

    insert_sql = text("""
        INSERT INTO dwd_sales_detail  (sale_id, sale_date, year, month, weekday, is_weekend,
             product_id, product_name, category,
             region, province, city,
             quantity, amount, cost, profit, dt)
        SELECT
            o.id                      AS sale_id,
            d.date                    AS sale_date,
            d.year, d.month, d.weekday, d.is_weekend,     -- 来自 dim_date
            o.product_id,
            p.product_name, p.category,                    -- 来自 dim_product
            r.region, r.province, r.city,                  -- 来自 dim_region
            o.quantity, o.amount, o.cost,
            o.amount - o.cost         AS profit,           -- 派生字段
            o.dt
        FROM ods_sales o
        JOIN dim_date    d ON o.date_id    = d.date_id
        JOIN dim_product p ON o.product_id = p.product_id
        JOIN dim_region  r ON o.region_id  = r.region_id
        WHERE o.dt = :bizdate
          AND o.amount >= 0        -- 清洗：过滤异常金额（防御性）
    """)

    try:
        # 先数 ODS 有多少行，用于对比
        ods_count = db.execute(
            text("SELECT COUNT(*) FROM ods_sales WHERE dt = :bizdate"),
            {"bizdate": bizdate},
        ).scalar() or 0
        db.execute(delete_sql, {"bizdate": bizdate})
        inserted = db.execute(insert_sql, {"bizdate": bizdate}).rowcount
        db.commit()

        if inserted > ods_count:
            logger.warning(
                f"[dwd_sales_detail] 行数异常膨胀: ods={ods_count}, dwd={inserted}"
            )

        dropped = ods_count - inserted
        logger.info(
            f"[dwd_sales_detail] bizdate={bizdate} ods={ods_count} "
            f"dwd={inserted} 清洗掉={dropped}"
        )
        return {'bizDate': bizdate, "insertTotal": inserted, "actCount": ods_count, "dropCount": dropped}

    except Exception:
        logger.exception(f"[dwd_sales_detail] bizdate={bizdate} 失败已回滚")
        raise


def run_dws_sales_daily(db: Session, bizdate: str) -> dict:
    """
    ----------
    db 数据库会话
    bizdate 跑批数据时间
    从数据仓库明细层获取数据仓库明细层 粒度为每日订单
    Returns 插入多少条
    -------
    """
    delete_sql = text("DELETE FROM dws_sales_daily WHERE dt=:bizdate")
    insert_sql = text("""
            INSERT INTO dws_sales_daily
                (dt, category, region, order_cnt, total_qty, total_amount, total_profit)
            SELECT
                :bizdate           AS dt,
                category,          -- 直接取，不用 JOIN dim_product
                region,            -- 直接取，不用 JOIN dim_region
                COUNT(*)           AS order_cnt,
                SUM(quantity)      AS total_qty,
                SUM(amount)        AS total_amount,
                SUM(profit)        AS total_profit   -- DWD 已算好，直接 SUM
            FROM dwd_sales_detail
            WHERE dt = :bizdate
            GROUP BY category, region
        """)
    try:
        db.execute(delete_sql, {"bizdate": bizdate})
        insertd = db.execute(insert_sql, {"bizdate": bizdate}).rowcount
        db.commit()
        logger.info(f"[dws_sales_daily] bizdate={bizdate} 插{insertd}行")
        return {"bizDate": bizdate, "insertTotal": insertd}
    except:
        db.rollback()
        logger.exception(f"[dws_sales_daily] bizdate={bizdate} 失败已回滚")
        raise


def run_dws_sales_daily_category(db: Session, bizdate: str) -> dict:
    """
    ----------
    db 数据库会话
    bizdate 跑批数据时间
    从数据仓库明细层获取数据仓库明细层 粒度为时间 分类
    Returns 插入多少条
    -------
    """
    delete_sql = text("DELETE FROM dws_sales_daily_category WHERE dt=:bizdate")
    insert_sql = text("""
     INSERT INTO dws_sales_daily_category
        (dt, category, order_cnt, total_qty, total_amount, total_profit)
     SELECT
        :bizdate          AS dt,
        category,
        COUNT(*)          AS order_cnt,
        SUM(quantity)     AS total_qty,
        SUM(amount)       AS total_amount,
        SUM(amount-cost)  AS total_profit
     FROM  dwd_sales_detail
     WHERE dt=:bizdate
     GROUP BY category
    """)
    try:
        db.execute(delete_sql, {"bizdate": bizdate})
        inserted = db.execute(insert_sql, {"bizdate": bizdate}).rowcount
        db.commit()
        logger.info(f"[dws_sales_daily_category] bizdate={bizdate} 插入{inserted}行")
        return {'bizDate': bizdate, 'insertTotal': inserted}
    except Exception:
        db.rollback()
        logger.exception(f"[dws_sales_daily] bizdate={bizdate} 失败已回滚")
        raise


def run_dws_sales_daily_monthly_region(db: Session, bizdate: str) -> dict:
    """
    ----------
    db 数据库会话
    bizdate 跑批数据时间
    从贴源层获取数据仓库明细层 粒度为月份 大区
    Returns 插入多少条
     -------
    """
    delete_sql = text("DELETE FROM dws_sales_monthly_region  WHERE month =:bizdate")
    insert_sql = text("""
        INSERT INTO dws_sales_monthly_region
        (month, region, order_cnt, total_qty, total_amount, total_profit)
        SELECT
            :bizdate                  AS month,
            f.region,
            COUNT(*)                AS order_cnt,
            SUM(f.quantity)         AS total_qty,
            SUM(f.amount)           AS total_amount,
            SUM(f.amount - f.cost)  AS total_profit
        FROM dwd_sales_detail f
        WHERE LEFT(f.dt, 6) = :bizdate
        GROUP BY f.region
    """)
    try:

        db.execute(delete_sql, {"bizdate": bizdate})
        inserted = db.execute(insert_sql, {"bizdate": bizdate}).rowcount
        db.commit()
        logger.info(f"[dws_sales_monthly_region] bizdate={bizdate} 插入{inserted}行")
        return {'bizDate': bizdate, 'insertTotal': inserted}
    except Exception:
        db.rollback()
        raise
