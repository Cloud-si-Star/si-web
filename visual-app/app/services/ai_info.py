from datetime import datetime, time
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.ai_info import AiInfo
from app.schemas.ai_info import AiInfoQuery, AiInfoItem, AiInfoPage, AiInfoUpdate


def _build_query(db: Session, cond: AiInfoQuery):
    """
    根据查询条件构建基础查询

    Args:
        db: 数据库会话
        cond: 查询条件

    Returns:
        查询对象
    """
    query = db.query(AiInfo)

    if cond.ai_name:
        query = query.filter(AiInfo.ai_name.like(f"%{cond.ai_name}%"))

    if cond.ai_status:
        query = query.filter(AiInfo.ai_status == cond.ai_status)

    if cond.ai_date:
        start = datetime.combine(cond.ai_date, time.min)
        end = datetime.combine(cond.ai_date, time.max)
        query = query.filter(and_(
            AiInfo.create_time >= start,
            AiInfo.create_time <= end
        ))

    return query


def get_ai_list(db: Session, cond: AiInfoQuery) -> AiInfoPage:
    """
    分页查询 AI 信息列表

    Args:
        db: 数据库会话
        cond: 查询条件

    Returns:
        分页结果对象
    """
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

    logger.info(
        "查询 AI 列表成功: total=%s, page=%s, page_size=%s",
        total,
        cond.page,
        cond.page_size
    )

    return AiInfoPage(
        list=data,
        total=total,
        page=cond.page,
        page_size=cond.page_size,
    )


def get_ai_by_id(db: Session, ai_id: int) -> Optional[AiInfo]:
    """
    根据 AI ID 获取记录

    Args:
        db: 数据库会话
        ai_id: AI 编号

    Returns:
        AI 信息对象，不存在返回 None
    """
    return db.query(AiInfo).filter(AiInfo.ai_id == ai_id).first()


def get_ai_by_id_or_raise(db: Session, ai_id: int) -> AiInfo:
    """
    根据 AI ID 获取记录，不存在则抛出异常

    Args:
        db: 数据库会话
        ai_id: AI 编号

    Returns:
        AI 信息对象

    Raises:
        ValueError: 记录不存在
    """
    obj = get_ai_by_id(db, ai_id)
    if not obj:
        raise ValueError(f"AI 记录不存在: ai_id={ai_id}")
    return obj


def update_ai_info(db: Session, payload: AiInfoUpdate) -> Optional[AiInfo]:
    """
    更新 AI 信息

    Args:
        db: 数据库会话
        payload: 更新数据

    Returns:
        更新后的对象，不存在返回 None
    """
    obj = db.query(AiInfo).filter(AiInfo.ai_id == payload.ai_id).first()
    if not obj:
        logger.warning(f"更新 AI 信息失败，记录不存在: ai_id={payload.ai_id}")
        return None

    # 排除 ai_id，它只是定位键
    update_data = payload.model_dump(exclude_unset=True, exclude={"ai_id"})

    for field, value in update_data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)

    logger.info(f"更新 AI 信息成功: ai_id={payload.ai_id}, fields={list(update_data.keys())}")

    return obj


def create_ai_info(
        db: Session,
        ai_id: int,
        ai_name: str,
        ai_status: str = "0",
        ai_use: int = 0,
        remark: str = None,
) -> AiInfo:
    """
    创建 AI 信息记录

    Args:
        db: 数据库会话
        ai_id: AI 编号
        ai_name: AI 名称
        ai_status: 状态（默认0=离线）
        ai_use: 使用次数（默认0）
        remark: 备注

    Returns:
        创建的对象
    """
    obj = AiInfo(
        ai_id=ai_id,
        ai_name=ai_name,
        ai_status=ai_status,
        ai_use=ai_use,
        remark=remark,
        create_time=datetime.now(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    logger.info(f"创建 AI 信息成功: ai_id={ai_id}, ai_name={ai_name}")

    return obj


def delete_ai_info(db: Session, ai_id: int) -> bool:
    """
    删除 AI 信息记录

    Args:
        db: 数据库会话
        ai_id: AI 编号

    Returns:
        是否删除成功
    """
    obj = db.query(AiInfo).filter(AiInfo.ai_id == ai_id).first()
    if not obj:
        logger.warning(f"删除 AI 信息失败，记录不存在: ai_id={ai_id}")
        return False

    db.delete(obj)
    db.commit()

    logger.info(f"删除 AI 信息成功: ai_id={ai_id}")

    return True
