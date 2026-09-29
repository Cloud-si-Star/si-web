"""
创建 file_record 表
运行方式: python -m app.scripts.create_file_record_table
"""
from sqlalchemy import text
from app.core.database import engine, Base
from app.models.file_record import FileRecord


def create_table():
    """创建表"""
    Base.metadata.create_all(bind=engine)
    print("表 file_record 创建成功！")


def drop_table():
    """删除表"""
    Base.metadata.drop_all(bind=engine)
    print("表 file_record 删除成功！")


def check_table_exists() -> bool:
    """检查表是否存在"""
    with engine.connect() as conn:
        result = conn.execute(
            text("SHOW TABLES LIKE 'file_record'")
        ).fetchone()
        return result is not None


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "drop":
            drop_table()
        elif sys.argv[1] == "recreate":
            if check_table_exists():
                drop_table()
            create_table()
        else:
            print("未知命令，可用: create, drop, recreate")
    else:
        if check_table_exists():
            print("表 file_record 已存在")
        else:
            create_table()
