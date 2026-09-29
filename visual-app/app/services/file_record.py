from datetime import datetime, time
from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.file_record import FileRecord
from app.schemas.file_record import FileRecordQuery, FileRecordItem, FileRecordPage, FileRecordCreate


def _build_query(db: Session, cond: FileRecordQuery):
    """根据查询条件构建基础查询"""
    query = db.query(FileRecord)

    if cond.file_name:
        query = query.filter(FileRecord.file_name.like(f"%{cond.file_name}%"))

    if cond.file_type:
        query = query.filter(FileRecord.file_type == cond.file_type)

    if cond.upload_user:
        query = query.filter(FileRecord.upload_user == cond.upload_user)

    if cond.start_date:
        start = datetime.combine(cond.start_date, time.min)
        query = query.filter(FileRecord.upload_time >= start)

    if cond.end_date:
        end = datetime.combine(cond.end_date, time.max)
        query = query.filter(FileRecord.upload_time <= end)

    return query


def get_file_list(db: Session, cond: FileRecordQuery) -> FileRecordPage:
    """分页查询文件记录"""
    query = _build_query(db, cond)

    total = query.count()

    offset = (cond.page - 1) * cond.page_size

    rows = (
        query.order_by(FileRecord.id.desc())
        .offset(offset)
        .limit(cond.page_size)
        .all()
    )

    data = [
        FileRecordItem(
            id=r.id,
            file_name=r.file_name,
            file_type=r.file_type,
            file_path=r.file_path,
            file_size=r.file_size,
            upload_user=r.upload_user,
            upload_time=r.upload_time.strftime("%Y-%m-%d %H:%M:%S") if r.upload_time else None,
            remark=r.remark,
        )
        for r in rows
    ]

    logger.info(
        "查询文件记录列表成功: total=%s, page=%s",
        total, cond.page
    )

    return FileRecordPage(
        list=data,
        total=total,
        page=cond.page,
        page_size=cond.page_size,
    )


def create_file_record(db: Session, payload: FileRecordCreate) -> FileRecord:
    """创建文件记录"""
    obj = FileRecord(
        file_name=payload.file_name,
        file_type=payload.file_type,
        file_path=payload.file_path,
        file_size=payload.file_size,
        upload_user=payload.upload_user,
        remark=payload.remark,
        upload_time=datetime.now(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    logger.info(
        "创建文件记录成功: id=%s, file_name=%s, upload_user=%s",
        obj.id, obj.file_name, obj.upload_user
    )

    return obj


def get_file_by_id(db: Session, file_id: int) -> Optional[FileRecord]:
    """根据ID获取文件记录"""
    return db.query(FileRecord).filter(FileRecord.id == file_id).first()


def delete_file_record(db: Session, file_id: int) -> bool:
    """删除文件记录"""
    obj = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if not obj:
        logger.warning(f"删除文件记录失败，记录不存在: id={file_id}")
        return False

    db.delete(obj)
    db.commit()

    logger.info(f"删除文件记录成功: id={file_id}")
    return True
