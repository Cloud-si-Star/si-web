import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

# 创建日志目录
LOG_DIR.mkdir(exist_ok=True)


# ➕ 新增：只保留异常堆栈最后 N 行的 Formatter
class TailFormatter(logging.Formatter):
    """异常堆栈只保留最后 N 行，避免第三方库刷屏"""
    MAX_TAIL_LINES = 5

    def formatException(self, ei):
        text = super().formatException(ei)
        lines = text.rstrip().splitlines()
        if len(lines) > self.MAX_TAIL_LINES:
            hidden = len(lines) - self.MAX_TAIL_LINES
            lines = [f"...(省略 {hidden} 行)"] + lines[-self.MAX_TAIL_LINES:]
        return "\n".join(lines)


# 日志格式
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ➕ 新增：统一 Formatter 实例（顺便用上 TailFormatter）
formatter = TailFormatter(LOG_FORMAT, DATE_FORMAT)

# 控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 文件处理器（按大小轮转）
file_handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# 错误日志处理器
error_file_handler = RotatingFileHandler(
    LOG_DIR / "error.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# 根日志配置
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[console_handler, file_handler, error_file_handler],
)

# 应用日志记录器
logger = logging.getLogger("app")

# SQLAlchemy 日志（可选，生产环境可关闭）
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
