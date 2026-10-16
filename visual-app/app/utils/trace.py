import traceback
from pathlib import Path

# 项目根目录（app 的上一级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # 按实际结构调整

# 明确排除的目录（venv、site-packages）
EXCLUDE = ("venv", "site-packages", "dist-packages", "Lib\\python", "Lib/python")


def _is_project_file(filename: str) -> bool:
    f = filename.replace("\\", "/")
    if any(x in f for x in EXCLUDE):
        return False
    try:
        return PROJECT_ROOT in Path(filename).resolve().parents
    except Exception:
        return False


def get_short_traceback(exc: Exception) -> str:
    """只保留本项目代码的调用帧"""
    frames = traceback.extract_tb(exc.__traceback__)
    project_frames = [f for f in frames if _is_project_file(f.filename)]

    # 兜底：如果项目帧为空，取最后 3 帧
    if not project_frames:
        project_frames = frames[-3:]

    lines = ["Traceback (只显示本项目代码):"]
    for f in project_frames:
        lines.append(f'  File "{f.filename}", line {f.lineno}, in {f.name}')
        if f.line:
            lines.append(f"    {f.line}")
    lines.append(f"{type(exc).__name__}: {exc}")
    return "\n".join(lines)
