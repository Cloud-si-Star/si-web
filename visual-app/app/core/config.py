from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    """应用配置"""
    app_name: str = "visual-app API"
    version: str = "1.0.0"

    # 项目根路径
    base_dir: Path = BASE_DIR


settings = Settings()
