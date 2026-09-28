from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ai_info import AiInfoPage, AiInfoQuery, AiInfoUpdate
from app.services import ai_info as ai_service

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

from fastapi import File, UploadFile, Form
import os
import uuid
from datetime import datetime

# 存储目录
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        type: str = Form(None),  # 对应前端 extraData 里的字段
):
    # 1. 基本校验
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    # 2. 限制后缀（按需改）
    ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".xlsx", ".docx", ".zip"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")

    # 3. 限制大小（如 10MB）—— 边读边判，避免一次性读入内存
    MAX_SIZE = 10 * 1024 * 1024
    size = 0

    # 4. 生成唯一文件名，避免覆盖
    save_name = f"{datetime.now():%Y%m%d%H%M%S}_{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, save_name)

    try:
        with open(save_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # 每次 1MB
                size += len(chunk)
                if size > MAX_SIZE:
                    f.close()
                    os.remove(save_path)
                    raise HTTPException(status_code=413, detail="文件超过 10MB")
                f.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")
    finally:
        await file.close()

    # 5. 返回你前端约定的 ApiResult 结构
    return success(data={"code": 0, "message": "更新成功"})


@router.patch("/list")
def update_ai(
        payload: AiInfoUpdate,
        db: Session = Depends(get_db),
):
    obj = ai_service.update_ai_info(db, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="记录不存在")
    return success(data={"code": 0, "message": "更新成功"})


@print_args(enable=True)
@router.get("/list", response_model=AiInfoPage)
def get_ai_list(
        cond: AiInfoQuery = Depends(),
        db: Session = Depends(get_db),
):
    """分页查询 AI 信息列表"""
    return ai_service.get_ai_list(db, cond)


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
