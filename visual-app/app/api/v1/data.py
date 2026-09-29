import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.file_record import FileRecordPage, FileRecordQuery, FileRecordCreate
from app.schemas.ai_info import AiInfoPage, AiInfoQuery
from app.schemas.response import ResponseModel, success
from app.services import ai_info as ai_service
from app.services import file_record as file_service
from app.models.file_record import FileRecord

router = APIRouter(prefix="/data", tags=["data"])

# 存储目录配置
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".xlsx", ".docx", ".zip"}
# 最大文件大小（10MB）
MAX_FILE_SIZE: int = 10 * 1024 * 1024
# 分块读取大小（1MB）
CHUNK_SIZE: int = 1024 * 1024


def validate_file_extension(filename: str) -> str:
    """校验文件扩展名"""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {ext}"
        )
    return ext


def generate_unique_filename(ext: str) -> str:
    """生成唯一文件名"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}{ext}"


async def save_upload_file(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> tuple:
    """
    保存上传文件，支持大文件流式写入和大小限制

    Returns:
        tuple: (save_path, file_size)
    """
    ext = validate_file_extension(file.filename)
    save_name = generate_unique_filename(ext)
    save_path = os.path.join(UPLOAD_DIR, save_name)

    size = 0
    try:
        with open(save_path, "wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                size += len(chunk)
                if size > max_size:
                    f.close()
                    os.remove(save_path)
                    raise HTTPException(
                        status_code=413,
                        detail=f"文件超过 {max_size // (1024 * 1024)}MB"
                    )
                f.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")
    finally:
        await file.close()

    return save_path, size


@router.post("/upload", response_model=ResponseModel)
async def upload_file(
        file: UploadFile = File(...),
        upload_user: Optional[str] = Form(None, description="上传用户"),
):
    """
    文件上传接口

    - 支持图片、文档、压缩包等格式
    - 单文件大小限制 10MB
    - 自动生成唯一文件名防止覆盖
    - 上传信息存入数据库
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    # 保存文件并获取文件大小
    save_path, file_size = await save_upload_file(file)

    # 获取文件扩展名作为类型
    ext = os.path.splitext(file.filename)[1].lower()

    return success(
        data={
            "code": 0,
            "message": "上传成功",
            "file_path": save_path,
            "file_name": os.path.basename(save_path),
            "file_type": ext,
            "file_size": file_size,
        }
    )


@router.post("/with-record", response_model=ResponseModel)
async def upload_file_with_record(
        file: UploadFile = File(...),
        upload_user: Optional[str] = Form(None, description="上传用户"),
        remark: Optional[str] = Form(None, description="备注"),
        db: Session = Depends(get_db),
):
    """
    文件上传接口（带数据库记录）

    - 支持图片、文档、压缩包等格式
    - 单文件大小限制 10MB
    - 自动生成唯一文件名防止覆盖
    - 上传信息存入数据库（文件类型、文件名称、上传时间、上传用户）
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    # 保存文件并获取文件大小
    save_path, file_size = await save_upload_file(file)

    # 获取原始文件名和扩展名
    original_filename = file.filename
    ext = os.path.splitext(original_filename)[1].lower()

    # 创建数据库记录
    record = FileRecordCreate(
        file_name=original_filename,
        file_type=ext,
        file_path=save_path,
        file_size=file_size,
        upload_user=upload_user,
        remark=remark,
    )

    db_record = file_service.create_file_record(db, record)

    return success(
        data={
            "code": 0,
            "message": "上传成功",
            "file_id": db_record.id,
            "file_path": save_path,
            "file_name": os.path.basename(save_path),
            "original_name": original_filename,
            "file_type": ext,
            "file_size": file_size,
            "upload_user": upload_user,
            "upload_time": db_record.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@router.get("/files", response_model=FileRecordPage)
def get_file_list(
        cond: FileRecordQuery = Depends(),
        db: Session = Depends(get_db),
):
    """
    分页查询文件记录列表

    - 支持按文件名、文件类型、上传用户模糊搜索
    - 支持按上传日期范围筛选
    - 支持分页
    """
    return file_service.get_file_list(db, cond)


@router.patch("/list", response_model=ResponseModel)
def update_ai(
        payload,
        db: Session = Depends(get_db),
):
    obj = ai_service.update_ai_info(db, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="记录不存在")
    return success(data={"code": 0, "message": "更新成功"})


@router.get("/list", response_model=AiInfoPage)
def get_ai_list(
        cond: AiInfoQuery = Depends(),
        db: Session = Depends(get_db),
):
    """分页查询 AI 信息列表"""
    return ai_service.get_ai_list(db, cond)
