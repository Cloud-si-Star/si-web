import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.file_record import FileRecordCreate, FileRecordPage, FileRecordQuery
from app.schemas.response import ResponseModel, success
from app.services import file_record as file_service

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".xlsx", ".docx", ".zip"}
MAX_FILE_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024


def validate_file_extension(filename: str) -> str:
    """Validate uploaded file extensions."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")
    return ext


def generate_unique_filename(ext: str) -> str:
    """Create a collision-resistant stored filename."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{uuid.uuid4().hex[:8]}{ext}"


async def save_upload_file(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> tuple[str, int]:
    """Save an upload in chunks and enforce the maximum file size."""
    ext = validate_file_extension(file.filename or "")
    save_path = os.path.join(UPLOAD_DIR, generate_unique_filename(ext))
    size = 0

    try:
        with open(save_path, "wb") as target:
            while chunk := await file.read(CHUNK_SIZE):
                size += len(chunk)
                if size > max_size:
                    raise HTTPException(
                        status_code=413,
                        detail=f"文件超过 {max_size // (1024 * 1024)}MB",
                    )
                target.write(chunk)
    except HTTPException:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise
    except OSError as error:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=f"保存失败: {error}") from error
    finally:
        await file.close()

    return save_path, size


@router.post("/content", response_model=ResponseModel)
async def upload_file_content(file: UploadFile = File(...)):
    """Upload a file without creating a database record."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    save_path, file_size = await save_upload_file(file)
    ext = os.path.splitext(file.filename)[1].lower()
    return success(data={
        "file_path": save_path,
        "file_name": os.path.basename(save_path),
        "file_type": ext,
        "file_size": file_size,
    }, message="上传成功")


@router.post("", response_model=ResponseModel, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    upload_user: Optional[str] = Form(None, description="上传用户"),
    remark: Optional[str] = Form(None, description="备注"),
    db: Session = Depends(get_db),
):
    """Upload a file and persist its metadata."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    original_filename = file.filename
    save_path, file_size = await save_upload_file(file)
    ext = os.path.splitext(original_filename)[1].lower()
    record = file_service.create_file_record(
        db,
        FileRecordCreate(
            file_name=original_filename,
            file_type=ext,
            file_path=save_path,
            file_size=file_size,
            upload_user=upload_user,
            remark=remark,
        ),
    )

    return success(data={
        "file_id": record.id,
        "file_path": save_path,
        "file_name": os.path.basename(save_path),
        "original_name": original_filename,
        "file_type": ext,
        "file_size": file_size,
        "upload_user": upload_user,
        "upload_time": record.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
    }, message="上传成功")


@router.get("", response_model=FileRecordPage)
def get_file_list(cond: FileRecordQuery = Depends(), db: Session = Depends(get_db)):
    """Return a filtered, paginated file-record list."""
    return file_service.get_file_list(db, cond)


@router.get("/{file_id}/content")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """Download a stored file using its database record ID."""
    record = file_service.get_file_by_id(db, file_id)
    if not record:
        raise HTTPException(status_code=404, detail="文件记录不存在")
    if not os.path.exists(record.file_path):
        raise HTTPException(status_code=404, detail="文件已被删除或不存在")

    return FileResponse(
        path=record.file_path,
        filename=record.file_name,
        media_type="application/octet-stream",
    )
