"""
ETL 业务服务层。
提供销售数据分层处理及事务控制。单日任务默认自行提交；
月度任务关闭逐日提交，全部日期成功后统一提交。
"""
import calendar
import logging
from datetime import datetime
from typing import Callable, TypedDict

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.logger import logger  # 用你已封装的 logger


class EtlDayResult(TypedDict, total=False):
    insertTotal: int
    bizDate: str
    dropCount: int
    actCount: int


class MonthlyDayResult(TypedDict):
    bizDate: str
    insertTotal: int
    dropCount: int


class MonthlyBatchResult(TypedDict):
    bizMonth: str
    startDate: str
    endDate: str
    totalDays: int
    insertTotal: int
    dropCount: int
    results: list[MonthlyDayResult]


MonthlyRunner = Callable[[Session, str, bool], int | EtlDayResult]


class EtlError(Exception):
    """ETL 执行失败异常，由 API 路由层转换为 HTTP 错误响应。"""
    pass


def validate_bizdate(bizdate: str) -> str:
    """校验业务日期是否为有效的 YYYYMMDD 日历日期。

    Args:
        bizdate: 待校验的业务日期。

    Returns:
        校验通过后原样返回业务日期。

    Raises:
        ValueError: 日期格式错误或不是有效日历日期。
    """
    try:
        datetime.strptime(bizdate, "%Y%m%d")
    except ValueError:
        # 理论上 Pydantic 已拦，这里兜底（service 可能被内部调用）
        raise ValueError(f"bizdate 格式错误，应为 YYYYMMDD: {bizdate}")
    return bizdate


'fact_sales->ods_sales->dwd_sales_detail->dws_sales_daily,dws_sales_daily_category,dws_sales_monthly_region'
'业务数据      贴源层      数据仓库明细层       数据仓库汇总层'


def run_ods_sales(db: Session, bizdate: str, commit_transaction: bool = True) -> int:
    """将指定日期的业务事实数据重建到 ODS 贴源层。

    先删除该日期的旧 ODS 数据，再从 fact_sales 重新抽取，重复执行不会
    累积重复记录。月度批处理可关闭逐日提交，由批处理统一提交事务。

    Args:
        db: 当前请求使用的数据库会话。
        bizdate: YYYYMMDD 格式的业务日期。
        commit_transaction: 是否在本日处理成功后立即提交。

    Returns:
        本次写入 ODS 的记录数。

    Raises:
        ValueError: 业务日期无效。
        Exception: SQL 执行失败；当前事务会回滚。
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
        if commit_transaction:
            db.commit()
        logger.info(f"[ods_sales] bizdate={bizdate} 抽{inserted}行")
        return inserted
    except Exception:

        db.rollback()
        logger.exception(f"[ods_sales] bizdate={bizdate} 失败已回滚")
        raise


def run_dwd_sales_detail(
        db: Session,
        bizdate: str,
        commit_transaction: bool = True,
) -> EtlDayResult:
    """从 ODS 加工指定日期的 DWD 销售明细。

    关联日期、商品和区域维度，过滤负金额记录并计算利润；返回插入数、
    ODS 原始数和过滤数。支持关闭逐日提交以参与月度原子事务。

    Args:
        db: 当前请求使用的数据库会话。
        bizdate: YYYYMMDD 格式的业务日期。
        commit_transaction: 是否在本日处理成功后立即提交。

    Returns:
        包含 bizDate、insertTotal、actCount 和 dropCount 的统计字典。

    Raises:
        Exception: SQL 执行失败；当前事务会回滚。
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
        if commit_transaction:
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
        db.rollback()
        logger.exception(f"[dwd_sales_detail] bizdate={bizdate} 失败已回滚")
        raise


def run_dws_sales_daily(
        db: Session,
        bizdate: str,
        commit_transaction: bool = True,
) -> EtlDayResult:
    """按指定业务日期重建日销量汇总数据。

    汇总 DWD 明细中的品类和区域维度指标；支持关闭逐日提交以参与月度
    原子事务。

    Args:
        db: 当前请求使用的数据库会话。
        bizdate: YYYYMMDD 格式的业务日期。
        commit_transaction: 是否在本日处理成功后立即提交。

    Returns:
        包含业务日期和插入记录数的统计字典。

    Raises:
        Exception: SQL 执行失败；当前事务会回滚。
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
        if commit_transaction:
            db.commit()
        logger.info(f"[dws_sales_daily] bizdate={bizdate} 插{insertd}行")
        return {"bizDate": bizdate, "insertTotal": insertd}
    except:
        db.rollback()
        logger.exception(f"[dws_sales_daily] bizdate={bizdate} 失败已回滚")
        raise


def run_dws_sales_daily_category(
        db: Session,
        bizdate: str,
        commit_transaction: bool = True,
) -> EtlDayResult:
    """按指定业务日期重建日品类汇总数据。

    汇总 DWD 明细中的品类级订单数、销量、销售额和利润；支持关闭逐日
    提交以参与月度原子事务。

    Args:
        db: 当前请求使用的数据库会话。
        bizdate: YYYYMMDD 格式的业务日期。
        commit_transaction: 是否在本日处理成功后立即提交。

    Returns:
        包含业务日期和插入记录数的统计字典。

    Raises:
        Exception: SQL 执行失败；当前事务会回滚。
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
        if commit_transaction:
            db.commit()
        logger.info(f"[dws_sales_daily_category] bizdate={bizdate} 插入{inserted}行")
        return {'bizDate': bizdate, 'insertTotal': inserted}
    except Exception:
        db.rollback()
        logger.exception(f"[dws_sales_daily] bizdate={bizdate} 失败已回滚")
        raise


def run_dws_sales_daily_monthly_region(db: Session, bizdate: str) -> EtlDayResult:
    """按 YYYYMM 重建指定月份的大区销售汇总。

    汇总该月 DWD 明细中各大区的订单数、销量、销售额和利润。

    Args:
        db: 当前请求使用的数据库会话。
        bizdate: YYYYMM 格式的业务月份。

    Returns:
        包含业务月份和插入记录数的统计字典。

    Raises:
        Exception: SQL 执行失败；当前事务会回滚。
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


def _run_monthly_sales_batch(
        db: Session,
        biz_month: str,
        task_name: str,
        runner: MonthlyRunner,
) -> MonthlyBatchResult:
    """在单个事务中逐日重跑整月 ETL，并汇总逐日结果。

    每日 service 调用均关闭自身提交；整月所有日期成功后统一提交。
    任一日处理或最终提交失败时，回滚本月所有写入。

    Args:
        db: 当前请求使用的数据库会话。
        biz_month: YYYYMM 格式的业务月份。
        task_name: 用于日志和错误消息的任务名称。
        runner: 支持 commit_transaction 参数的单日 ETL service 方法。

    Returns:
        含月份、起止日期、自然日总数、累计写入/丢弃数和逐日明细的字典。

    Raises:
        ValueError: 月份格式错误或不是有效月份。
        EtlError: 月内任一天处理失败，且整月事务已回滚。
    """
    if len(biz_month) != 6 or not biz_month.isdigit():
        raise ValueError("bizMonth 必须是有效的 YYYYMM 月份")

    try:
        month_start = datetime.strptime(biz_month, "%Y%m").date().replace(day=1)
    except ValueError as error:
        raise ValueError("bizMonth 必须是有效的 YYYYMM 月份") from error

    total_days = calendar.monthrange(month_start.year, month_start.month)[1]
    results: list[MonthlyDayResult] = []
    try:
        for day in range(1, total_days + 1):
            bizdate = month_start.replace(day=day).strftime("%Y%m%d")
            output = runner(db, bizdate, False)
            if isinstance(output, int):
                inserted, dropped = output, 0
            else:
                inserted = output.get("insertTotal", 0)
                dropped = output.get("dropCount", 0)
            results.append({
                "bizDate": bizdate,
                "insertTotal": inserted,
                "dropCount": dropped,
            })
        db.commit()
    except Exception as error:
        db.rollback()
        logger.exception("[ETL] %s 月度处理失败 month=%s，已回滚", task_name, biz_month)
        raise EtlError(
            f"{task_name} {biz_month} 月处理失败，数据已回滚，请查看服务日志"
        ) from error

    return {
        "bizMonth": biz_month,
        "startDate": month_start.strftime("%Y%m%d"),
        "endDate": month_start.replace(day=total_days).strftime("%Y%m%d"),
        "totalDays": total_days,
        "insertTotal": sum(result["insertTotal"] for result in results),
        "dropCount": sum(result["dropCount"] for result in results),
        "results": results,
    }


def run_ods_sales_monthly(db: Session, biz_month: str) -> MonthlyBatchResult:
    """按自然月逐日重建 ODS 数据，并在整月成功后统一提交。

    Args:
        db: 当前请求使用的数据库会话。
        biz_month: YYYYMM 格式的业务月份。

    Returns:
        包含整月范围及逐日执行统计的结果。

    Raises:
        ValueError: 业务月份无效。
        EtlError: 任一日期处理失败，整月事务已回滚。
    """
    return _run_monthly_sales_batch(db, biz_month, "ODS", run_ods_sales)


def run_dwd_sales_detail_monthly(db: Session, biz_month: str) -> MonthlyBatchResult:
    """按自然月逐日重建 DWD 明细，并在整月成功后统一提交。

    Args:
        db: 当前请求使用的数据库会话。
        biz_month: YYYYMM 格式的业务月份。

    Returns:
        包含整月范围及逐日执行统计的结果。

    Raises:
        ValueError: 业务月份无效。
        EtlError: 任一日期处理失败，整月事务已回滚。
    """
    return _run_monthly_sales_batch(db, biz_month, "DWD", run_dwd_sales_detail)


def run_dws_sales_daily_monthly(db: Session, biz_month: str) -> MonthlyBatchResult:
    """按自然月逐日重建日销量汇总，并在整月成功后统一提交。

    Args:
        db: 当前请求使用的数据库会话。
        biz_month: YYYYMM 格式的业务月份。

    Returns:
        包含整月范围及逐日执行统计的结果。

    Raises:
        ValueError: 业务月份无效。
        EtlError: 任一日期处理失败，整月事务已回滚。
    """
    return _run_monthly_sales_batch(db, biz_month, "日销量汇总", run_dws_sales_daily)


def run_dws_sales_daily_category_monthly(db: Session, biz_month: str) -> MonthlyBatchResult:
    """按自然月逐日重建日品类汇总，并在整月成功后统一提交。

    Args:
        db: 当前请求使用的数据库会话。
        biz_month: YYYYMM 格式的业务月份。

    Returns:
        包含整月范围及逐日执行统计的结果。

    Raises:
        ValueError: 业务月份无效。
        EtlError: 任一日期处理失败，整月事务已回滚。
    """
    return _run_monthly_sales_batch(
        db, biz_month, "日品类汇总", run_dws_sales_daily_category,
    )


def run_ads_sales_monthly_report(db: Session, month: str) -> int:
    """重建指定月份的 ADS 销售报告及其环比、同比和区域排名指标。

    读取目标月份及去年同月的 DWD 数据，计算目标月区域指标后替换旧报告。

    Args:
        db: 当前请求使用的数据库会话。
        month: YYYYMM 格式的报告月份。

    Returns:
        本次写入 ADS 月报的记录数。

    Raises:
        Exception: SQL 执行失败；当前事务会回滚。
    """
    year, mon = int(month[:4], int(month[4:6]))
    month_start = f"{month}01"
    if mon == 12:
        next_month_start = f"{year + 1}0101"
    else:
        next_month_start = f"{year}{mon + 1:02d}01"

    delete_sql = text("DELETE FROM ads_sales_monthly_report WHERE month=:month")
    # 核心 SQL：分三层 CTE
    # ① base：原子指标（月 × 大区）
    # ② with_lag：加环比、同比（窗口函数）
    # ③ 最终：加毛利率、排名
    insert_sql = text("""
        INSERT INTO ads_sales_monthly_report
        (month, region, total_amount, total_profit, order_cnt,gross_margin_pct, mom_pct, yoy_pct, rank_in_region)
        WITH base AS(
            SELECT
                 CONCAT(d.year,LPAD(d.month,2,'0')) AS ym,
                 region,
                 SUM(amount) AS total_amount,
                 SUM(profit) AS total_profit,
                 COUNT(*)    AS order_cnt
            FROM dwd_sales_detail d
            WHERE d.dt >=:last_year_start AND d.dt<:next_mont_start
            GROUP BY d.year,d.month,region
        ),
        with_lag AS(
            SELECT 
                ym,region,total_amount,total_profit,order_cnt,
                LAG(total_amount,1)  OVER(PARTITION BY region ORDER BY ym) AS prev_amount,
                LAG(total_amount,12) OVER(PARTITION BY region ORDER BY ym) AS last_year_amount
            FROM base
        )
        SELECT
            ym                          AS month,
            region,
            total_amount,
            total_profit,
            order_cnt,
            -- 毛利率：NULLIF 防除零
            ROUND(total_profit / NULLIF(total_amount, 0) * 100, 2) AS gross_margin_pct,
            -- 环比：(本期-上期)/上期*100，上期为 NULL 时结果为 NULL
            ROUND((total_amount - prev_amount) / NULLIF(prev_amount, 0) * 100, 2) AS mom_pct,
            -- 同比：同上，但对比去年同月
            ROUND((total_amount - last_year_amount) / NULLIF(last_year_amount, 0) * 100, 2) AS yoy_pct,
            -- 大区内排名：只在目标月份内排名（过滤在 SELECT 外层做太晚，这里先用 RANK 再过滤）
            RANK() OVER (PARTITION BY ym ORDER BY total_amount DESC) AS rank_in_region
        FROM with_lag
        -- 只写目标月份的数据（base 里覆盖了去年同月，这里过滤掉）
        WHERE ym = :month
    """)
    try:
        db.execute(delete_sql, {"month": month})
        inserted = db.execute(insert_sql, {
            "month": month,
            "last_year_start": f"{year - 1}{mon:02d}01",  # 去年同月1号
            "next_month_start": next_month_start

        }).rowcount
        db.commit()
        logger.info(f"[ads_monthly_report] month={month} 插{inserted}行")
        return inserted
    except Exception:
        db.rollback()
        raise
