from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai_info import AIbyMonthChemas, AiInfoItem, AiInfoQuery, AiInfoUpdate, ProvinceChemas
from app.schemas.response import ResponseModel, success
from app.services import ai_info as ai_service

router = APIRouter(tags=["ai-usage"])


@router.get("/ai/models")
def get_ai_models(cond: AiInfoQuery = Depends(), db: Session = Depends(get_db)):
    """List AI model metadata with pagination and optional filters."""
    return ai_service.get_ai_list(db, cond)


@router.patch("/ai/models/{ai_id}", response_model=ResponseModel[AiInfoItem])
def update_ai_model(ai_id: int, payload: AiInfoUpdate, db: Session = Depends(get_db)):
    """Partially update an AI model record."""
    if payload.ai_id != ai_id:
        raise HTTPException(status_code=422, detail="路径 ai_id 与请求体 ai_id 不一致")
    model = ai_service.update_ai_info(db, payload)
    if not model:
        raise HTTPException(status_code=404, detail="记录不存在")
    return success(data=AiInfoItem.model_validate(model), message="更新成功")


@router.post("/ai/usage/distributions", response_model=ResponseModel, status_code=201)
def create_ai_usage_distribution(db: Session = Depends(get_db)):
    """Generate the next batch of AI usage distribution data."""
    ai_service.create_ai_use_distribution(db)
    return success(data={"message": "数据输入完成"}, message="数据输入完成")


@router.get("/ai/usage/provinces", response_model=ResponseModel)
def get_usage_by_province(db: Session = Depends(get_db)):
    """Aggregate AI usage totals by province."""
    return success(data=ai_service.sql_fetch_ai_use_total_grounp_by_province(db))


@router.get("/ai/usage/provinces/{province_id}/models", response_model=ResponseModel)
def get_usage_by_province_and_model(province_id: int, db: Session = Depends(get_db)):
    """Aggregate model usage for one province."""
    return success(data=ai_service.use_total_by_province_id(province_id, db))


@router.post("/ai/provinces", response_model=ResponseModel, status_code=201)
def create_provinces(province_ids: list[ProvinceChemas], db: Session = Depends(get_db)):
    """Insert province records used by the AI distribution reports."""
    ai_service.province_type_id(
        [province.model_dump() for province in province_ids],
        db,
    )
    return success(message="省份数据写入完成")


@router.get("/ai/usage/monthly", response_model=ResponseModel)
def get_monthly_usage(payload: AIbyMonthChemas = Depends(), db: Session = Depends(get_db)):
    """Return monthly usage for a province and AI model."""
    return success(data=ai_service.detail_by_aiIds_provinceIds(payload, db))


@router.get("/ai/usage/models", response_model=ResponseModel)
def get_usage_by_model(db: Session = Depends(get_db)):
    """Aggregate total usage for each AI model."""
    return success(data=ai_service.back_detail_by_all(db))
