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

aiTable = [
    {
        "ai_id": 52817,
        "ai_name": "DeepSeek",
        "ai_use": 892341,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2026-01-12 09:24:10",
        "remark": "国产开源大模型，支持代码与长文本"
    },
    {
        "ai_id": 31204,
        "ai_name": "ChatGPT",
        "ai_use": 1523876,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2025-11-03 14:10:55",
        "remark": "通用对话模型，多场景能力强"
    },
    {
        "ai_id": 74619,
        "ai_name": "Claude",
        "ai_use": 734219,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2025-12-20 11:33:22",
        "remark": "超大上下文窗口，适合文档分析"
    },
    {
        "ai_id": 19083,
        "ai_name": "Gemini",
        "ai_use": 612874,
        "ai_status": "offline",
        "ai_status_code": 0,
        "create_time": "2026-02-05 16:45:18",
        "remark": "多模态模型，当前版本维护中"
    },
    {
        "ai_id": 60527,
        "ai_name": "通义千问",
        "ai_use": 423110,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2026-01-28 10:12:44",
        "remark": "阿里自研大模型，中文优化较好"
    },
    {
        "ai_id": 45123,
        "ai_name": "文心一言",
        "ai_use": 389201,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2025-10-15 08:55:30",
        "remark": "百度生成式AI，知识检索能力强"
    },
    {
        "ai_id": 88345,
        "ai_name": "星火大模型",
        "ai_use": 276543,
        "ai_status": "offline",
        "ai_status_code": 0,
        "create_time": "2026-02-18 15:20:11",
        "remark": "讯飞模型，语音相关能力突出，版本升级暂停服务"
    },
    {
        "ai_id": 22109,
        "ai_name": "Llama3",
        "ai_use": 198740,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2026-03-01 09:10:25",
        "remark": "Meta开源模型，本地部署常用"
    },
    {
        "ai_id": 33782,
        "ai_name": "Qwen2",
        "ai_use": 165320,
        "ai_status": "online",
        "ai_status_code": 1,
        "create_time": "2026-03-10 14:30:07",
        "remark": "开源轻量化模型，推理速度快"
    },
    {
        "ai_id": 90147,
        "ai_name": "GLM4",
        "ai_use": 241356,
        "ai_status": "offline",
        "ai_status_code": 0,
        "create_time": "2026-02-22 17:05:42",
        "remark": "智谱AI，接口服务器迁移维护"
    }
]


@router.get('/list', response_model=ResponseModel)
def get_ai_list(
        ai_name: str | None = Query(None),
        ai_status: str | None = Query(None),
        ai_date: str | None = Query(None),
        page: int | None = Query(1),
        pageSize: int | None = Query(10),
):
    print(ai_name, ai_status, ai_date, page, pageSize)
    return success(data={"list": aiTable, "total": len(aiTable), "page": 1, "pageSize": 10})


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
