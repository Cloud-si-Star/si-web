from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.scripts.seek import run_seed
from app.schemas.response import success
from datetime import date

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get('/batch', summary="批量造数据")
def create_seed(db: Session = Depends(get_db)):
    run_seed(db, start=date(2025, 1, 1), end=date(2026, 10, 10))
    return success()
