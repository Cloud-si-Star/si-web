from pathlib import Path

# 项目根目录：window-ae/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# CSV 数据目录：window-ae/data/
DATA_DIR = BASE_DIR / "data"


class Settings:
    app_name: str = "window-ae API"
    version: str = "0.1.0"
    data_dir: Path = DATA_DIR


settings = Settings()
