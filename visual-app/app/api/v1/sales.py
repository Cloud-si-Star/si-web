from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.scripts.seek import run_seed
from app.services import analysis_service
from app.schemas.response import success
from app.core.logger import logger
from datetime import date

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get('/batch', summary="批量造数据")
def create_seed(db: Session = Depends(get_db)):
    run_seed(db, start=date(2025, 1, 1), end=date(2026, 10, 10))
    return success()


@router.get('/biz', summary="批量跑数据")
def create_dws(bizdate: str, db: Session = Depends(get_db)):
    logger.info(f"[API] 收到 ETL 请求 bizdate={bizdate}")
    try:
        inserted = analysis_service.run_dws_sales_daily(db, bizdate)
        logger.info(f"[API] ETL 成功 bizdate={bizdate}, inserted={inserted}")
        return success()
    except ValueError as e:
        logger.warning(f"[API] 参数非法 bizdate={bizdate}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 兜底：未预期异常
        logger.error(f"[API] 未预期异常 bizdate={bizdate}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="内部错误")
