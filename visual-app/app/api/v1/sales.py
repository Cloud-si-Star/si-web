from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.scripts.seek import run_seed
from app.services import analysis_service
from app.schemas.response import success
from app.core.logger import logger
from datetime import date

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/seeds", summary="批量生成销售数据")
def create_seed(db: Session = Depends(get_db)):
    run_seed(db, start=date(2025, 1, 1), end=date(2026, 10, 10))
    return success(message="销售数据生成完成")


@router.post("/daily-etl", summary="执行日销售汇总")
def create_dws(bizdate: str, db: Session = Depends(get_db)):
    logger.info(f"[API] 收到 ETL 请求 bizdate={bizdate}")
    try:
        inserted = analysis_service.run_dws_sales_daily(db, bizdate)
        logger.info(f"[API] ETL 成功 bizdate={bizdate}, inserted={inserted}")
        db.commit()
        return success(data={"inserted": inserted})
    except ValueError as e:
        logger.warning(f"[API] 参数非法 bizdate={bizdate}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        # 兜底：未预期异常
        logger.error(f"[API] 未预期异常 bizdate={bizdate}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="内部错误")


@router.post("/api/etl/ods/run")
def run_ods(
        bizdate: str = Query(..., pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    """ODS 抽取：fact_sales → ods_sales"""
    try:
        rows = analysis_service.etl_ods_sales(db, bizdate)
        return {"code": 0, "layer": "ODS", "bizdate": bizdate, "rows": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ODS 抽取失败: {e}")


'/api/v1/sales/api/etl/dwd/run'


@router.post("/api/etl/dwd/run")
def run_dwd(
        bizdate: str = Query(..., pattern=r"^\d{8}$"),
        db: Session = Depends(get_db),
):
    """DWD 加工：ods_sales → dwd_sales_detail，返回质量指标"""
    try:
        result = analysis_service.etl_dwd_sales_detail(db, bizdate)
        return {"code": 0, "layer": "DWD", "bizdate": bizdate, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DWD 加工失败: {e}")
