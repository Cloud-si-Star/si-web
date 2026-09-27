from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.ai_info import AiInfo

from app.schemas.response import ResponseModel, success
from app.services.csv_service import (
    read_csv,
    read_csv_paginated,
    stats_csv,
    list_csv_files,
    pie_csv_read,
    print_args
)

router = APIRouter(prefix="/data", tags=["data"])


@router.get('/list', response_model=ResponseModel)
@print_args(enable=True)
def get_ai_list(
        ai_name: str | None = Query(None),
        ai_status: str | None = Query(None),
        ai_date: str | None = Query(None),
        page: int = Query(1, ge=1),
        pageSize: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db),
):
    # 1. 基础查询
    query = db.query(AiInfo)

    # 2. 条件筛选
    if ai_name:
        # 模糊匹配名称
        query = query.filter(AiInfo.ai_name.like(f"%{ai_name}%"))

    if ai_status:
        # 状态文本精确匹配
        query = query.filter(AiInfo.ai_status == ai_status)

    if ai_date:
        # 按创建日期筛选，ai_date 传 "2026-02-22" 这种
        try:
            day = datetime.strptime(ai_date, "%Y-%m-%d").date()
            query = query.filter(
                AiInfo.create_time >= datetime.combine(day, datetime.min.time()),
                AiInfo.create_time < datetime.combine(day, datetime.max.time()),
            )
        except ValueError:
            # 日期格式不对就忽略该条件，避免 500
            pass

    # 3. 总数（要在分页前算）
    total = query.count()

    # 4. 分页
    offset = (page - 1) * pageSize
    rows = (
        query.order_by(AiInfo.id.desc())
        .offset(offset)
        .limit(pageSize)
        .all()
    )

    # 5. 转成 dict，避免 ORM 对象直接序列化
    data_list = [
        {
            "id": r.id,
            "ai_id": r.ai_id,
            "ai_name": r.ai_name,
            "ai_use": r.ai_use,
            "ai_status": r.ai_status,
            "ai_status_code": r.ai_status_code,
            "create_time": r.create_time.strftime("%Y-%m-%d %H:%M:%S") if r.create_time else None,
            "remark": r.remark,
        }
        for r in rows
    ]

    return success(
        data={
            "list": data_list,
            "total": total,
            "page": page,
            "pageSize": pageSize,
        }
    )


@router.get("/files", response_model=ResponseModel)
def get_csv_files():
    """获取 data 目录下所有 csv 文件列表"""
    files = list_csv_files()
    return success(data=files)


@router.get("/pie/{filename}", response_model=ResponseModel)
def get_csv_files(filename: str, description="统计返回，估计会报错"):
    """获取 data 目录下所有 csv 文件列表"""
    rows = pie_csv_read(filename)
    return success(data=rows)


@router.get("/csv/{filename}", response_model=ResponseModel)
def get_csv_content(
        filename: str,
        limit: int | None = Query(None, ge=1, description="最大返回条数，缺省返回全部"),
):
    """读取指定 csv 文件内容并返回给前端（可用 limit 限制条数）"""
    rows = read_csv(filename, limit=limit)
    return success(data={"filename": filename, "total": len(rows), "rows": rows})


@router.get("/csv/{filename}/page", response_model=ResponseModel)
def get_csv_page(
        filename: str,
        page: int = Query(1, ge=1, description="页码，从 1 开始"),
        page_size: int = Query(50, ge=1, le=1000, description="每页条数，最大 1000"),
):
    """分页读取 csv，适合大文件"""
    data = read_csv_paginated(filename, page=page, page_size=page_size)
    return success(data=data)


@router.get("/csv/{filename}/stats", response_model=ResponseModel)
def get_csv_stats(
        filename: str,
        group_by: str = Query(..., description="分组列名"),
        agg: str = Query("count", description="聚合方式: count/sum/mean/min/max/median"),
        metric: str | None = Query(None, description="数值列名，非 count 聚合时必填"),
        top: int | None = Query(None, ge=1, description="只返回结果最大的前 N 组"),
):
    """按列分组统计 csv 后返回结果"""
    data = stats_csv(filename, group_by=group_by, agg=agg, metric=metric, top=top)
    return success(data=data)
