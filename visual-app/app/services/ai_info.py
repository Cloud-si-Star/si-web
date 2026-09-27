from datetime import datetime, time
from sqlalchemy.orm import Session

from app.models.ai_info import AiInfo
from app.schemas.ai_info import AiInfoQuery, AiInfoItem, AiInfoPage, AiInfoUpdate
from app.core.logger import logger


def _build_query(db: Session, cond: AiInfoQuery):
    """根据条件构造基础查询"""
    query = db.query(AiInfo)

    if cond.ai_name:
        query = query.filter(AiInfo.ai_name.like(f"%{cond.ai_name}%"))

    if cond.ai_status:
        query = query.filter(AiInfo.ai_status == cond.ai_status)

    if cond.ai_date:
        start = datetime.combine(cond.ai_date, time.min)
        end = datetime.combine(cond.ai_date, time.max)
        query = query.filter(AiInfo.create_time.between(start, end))

    return query


def get_ai_list(db: Session, cond: AiInfoQuery) -> AiInfoPage:
    """分页查询 AI 信息"""
    query = _build_query(db, cond)

    total = query.count()

    offset = (cond.page - 1) * cond.page_size

    rows = (
        query.order_by(AiInfo.id.desc())
        .offset(offset)
        .limit(cond.page_size)
        .all()
    )

    data = [
        AiInfoItem(
            id=r.id,
            ai_id=r.ai_id,
            ai_name=r.ai_name,
            ai_use=r.ai_use,
            ai_status=r.ai_status,
            create_time=r.create_time.strftime("%Y-%m-%d %H:%M:%S") if r.create_time else None,
            remark=r.remark,
        )
        for r in rows
    ]

    logger.info("查询 AI 列表: total=%s, page=%s", total, cond.page)

    return AiInfoPage(
        list=data,
        total=total,
        page=cond.page,
        page_size=cond.page_size,
    )


# 更新数据
def update_ai_info(db: Session, payload: AiInfoUpdate) -> AiInfo | None:
    obj = db.query(AiInfo).filter(AiInfo.ai_id == payload.ai_id).first()
    if not obj:
        return None

    # 排除 ai_id，它不是更新字段，只是定位键
    update_data = payload.model_dump(exclude_unset=True, exclude={"ai_id"})

    for field, value in update_data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj
