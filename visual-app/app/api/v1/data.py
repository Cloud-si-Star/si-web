from fastapi import APIRouter, Query

from app.schemas.response import ResponseModel, success
from app.services.csv_service import (
    read_csv,
    read_csv_paginated,
    stats_csv,
    list_csv_files,
    pie_csv_read
)

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/files", response_model=ResponseModel)
def get_csv_files():
    """获取 data 目录下所有 csv 文件列表"""
    files = list_csv_files()
    return success(data=files)

@router.get("/pie/{filename}", response_model=ResponseModel)
def get_csv_files(filename: str,description="统计返回，估计会报错"):
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
