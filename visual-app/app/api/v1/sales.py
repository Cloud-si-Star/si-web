from datetime import date, datetime, timedelta
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.scripts.seek import run_seed
from app.services import analysis_service
from app.schemas.response import success, ResponseModel
from app.schemas.etl import BizResponse, MonthlyBizResponse
from app.core.logger import logger

router = APIRouter(prefix="/sales", tags=["sales"])
MAX_ODS_RANGE_DAYS = 31


@router.post("/seeds", summary="批量生成销售数据")
def create_seed(db: Session = Depends(get_db)):
    run_seed(db, start=date(2025, 1, 1), end=date(2026, 10, 10))
    return success(message="销售数据生成完成")


"""
route_run_ods_sales
route_run_dwd_sales_detail
route_run_dws_sales_daily
route_run_dws_sales_daily_category
route_run_dws_sales_monthly_region

ods-sales
dwd-sales-detail
dws-sales-daily
dws-sales-daily-category
dws-sales-monthly-region

"""


@router.post("/ods-sales", summary="执行贴源层数据", response_model=ResponseModel[BizResponse])
def route_run_ods_sales(
        bizdate: str = Query(..., pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    rows = analysis_service.run_ods_sales(db, bizdate)
    return success(data={'bizDate': bizdate, 'insertTotal': rows}, message="执行贴源层数据成功")


def _run_monthly_endpoint(
        db: Session,
        biz_month: str,
        runner: Callable[[Session, str], analysis_service.MonthlyBatchResult],
) -> ResponseModel[MonthlyBizResponse]:
    """Convert monthly service validation and ETL errors to HTTP responses."""
    try:
        result = runner(db, biz_month)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except analysis_service.EtlError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    return success(
        data=MonthlyBizResponse(**result),
        message=f"{biz_month} 月度批处理完成",
    )


@router.post("/ods-sales/monthly", summary="按月执行贴源层数据", response_model=ResponseModel[MonthlyBizResponse])
def route_run_ods_sales_monthly(
        biz_month: str = Query(..., alias="bizMonth", pattern=r"^\d{6}$"),
        db: Session = Depends(get_db),
):
    return _run_monthly_endpoint(db, biz_month, analysis_service.run_ods_sales_monthly)


@router.post("/ods-sales/range", summary="按日期范围逐日执行贴源层数据")
def route_run_ods_sales_range(
        start_date: str = Query(..., alias="startDate", pattern=r"^\d{8}$"),
        end_date: str = Query(..., alias="endDate", pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    """Run ODS extraction once per date in an inclusive, limited date range."""
    try:
        start = datetime.strptime(start_date, "%Y%m%d").date()
        end = datetime.strptime(end_date, "%Y%m%d").date()
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail="startDate 和 endDate 必须是有效的 YYYYMMDD 日期",
        ) from error

    if end < start:
        raise HTTPException(status_code=422, detail="endDate 不能早于 startDate")

    total_days = (end - start).days + 1
    if total_days > MAX_ODS_RANGE_DAYS:
        raise HTTPException(
            status_code=422,
            detail=f"单次最多处理 {MAX_ODS_RANGE_DAYS} 天",
        )

    results = []
    current_date = start
    while current_date <= end:
        bizdate = current_date.strftime("%Y%m%d")
        try:
            inserted = analysis_service.run_ods_sales(db, bizdate)
            results.append({
                "bizDate": bizdate,
                "status": "success",
                "insertTotal": inserted,
                "message": "执行成功",
            })
        except Exception:
            logger.exception("[ETL] ods_sales 范围处理失败 bizdate=%s", bizdate)
            results.append({
                "bizDate": bizdate,
                "status": "failed",
                "insertTotal": 0,
                "message": "处理失败，请查看服务日志",
            })
        current_date += timedelta(days=1)

    success_days = sum(result["status"] == "success" for result in results)
    failed_days = total_days - success_days
    return success(data={
        "startDate": start_date,
        "endDate": end_date,
        "totalDays": total_days,
        "successDays": success_days,
        "failedDays": failed_days,
        "totalInserted": sum(result["insertTotal"] for result in results),
        "results": results,
    }, message="ODS 范围批处理完成")


@router.post("/dwd-sales-detail", summary="执行数据仓库明细层", response_model=ResponseModel[BizResponse])
def route_run_dwd_sales_detail(
        bizdate: str = Query(..., pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    rows = analysis_service.run_dwd_sales_detail(db, bizdate)
    return success(data=BizResponse(**rows))


@router.post("/dwd-sales-detail/monthly", summary="按月执行数据仓库明细层",
             response_model=ResponseModel[MonthlyBizResponse])
def route_run_dwd_sales_detail_monthly(
        biz_month: str = Query(..., alias="bizMonth", pattern=r"^\d{6}$"),
        db: Session = Depends(get_db),
):
    return _run_monthly_endpoint(db, biz_month, analysis_service.run_dwd_sales_detail_monthly)


@router.post("/dws-sales-daily", summary="执行数据汇总层-日销量", response_model=ResponseModel[BizResponse])
def route_run_dws_sales_daily(
        bizdate: str = Query(..., pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    rows = analysis_service.run_dws_sales_daily(db, bizdate)
    return success(data=BizResponse(**rows))


@router.post("/dws-sales-daily/monthly", summary="按月执行日销量汇总",
             response_model=ResponseModel[MonthlyBizResponse])
def route_run_dws_sales_daily_monthly(
        biz_month: str = Query(..., alias="bizMonth", pattern=r"^\d{6}$"),
        db: Session = Depends(get_db),
):
    return _run_monthly_endpoint(db, biz_month, analysis_service.run_dws_sales_daily_monthly)


@router.post("/dws-sales-daily-category", summary="执行数据汇总层-日销量x大类",
             response_model=ResponseModel[BizResponse])
def route_run_dws_sales_daily_category(
        bizdate: str = Query(..., pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    rows = analysis_service.run_dws_sales_daily_category(db, bizdate)
    return success(data=BizResponse(**rows))


@router.post("/dws-sales-daily-category/monthly", summary="按月执行日品类汇总",
             response_model=ResponseModel[MonthlyBizResponse])
def route_run_dws_sales_daily_category_monthly(
        biz_month: str = Query(..., alias="bizMonth", pattern=r"^\d{6}$"),
        db: Session = Depends(get_db),
):
    return _run_monthly_endpoint(
        db, biz_month, analysis_service.run_dws_sales_daily_category_monthly,
    )


@router.post("/dws-sales-monthly-region", summary="执行数据汇总层-月份x大区", response_model=ResponseModel[BizResponse])
def route_run_dws_sales_monthly_region(
        bizdate: str = Query(..., pattern=r"^\d{6}$"),
        db: Session = Depends(get_db),
):
    rows = analysis_service.run_dws_sales_daily_monthly_region(db, bizdate)
    return success(data=BizResponse(**rows))
