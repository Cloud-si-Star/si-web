from datetime import datetime

from app.core.database import SessionLocal
from app.models.ai_info import AiInfo
from sqlalchemy import text
from app.core.database import engine


def drop_ai_status_code():
    """删除 ai_info 表的 ai_status_code 字段"""
    sql = "ALTER TABLE ai_info DROP COLUMN ai_status_code"
    with engine.begin() as conn:  # begin() 自动提交，出错自动回滚
        conn.execute(text(sql))
    print("ai_status_code 字段已删除")


def update_all_status():
    """把所有 AI 的状态统一更新"""
    db = SessionLocal()
    try:
        db.query(AiInfo).update(
            {AiInfo.ai_status: 1},
            synchronize_session=False,
        )
        db.commit()
    except Exception as e:
        print(e)
    finally:
        db.close()


def insert_ai_info(data_list: list):
    """
    批量入库
    data_list: 字典列表，每个字典对应一行
    返回：成功写入的条数
    """
    db = SessionLocal()
    try:
        objs = []
        for item in data_list:
            # create_time 是字符串，转成 datetime
            create_time = item.get("create_time")
            if isinstance(create_time, str):
                create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")

            objs.append(
                AiInfo(
                    ai_id=item.get("ai_id"),
                    ai_name=item.get("ai_name"),
                    ai_use=item.get("ai_use", 0),
                    ai_status=item.get("ai_status"),
                    ai_status_code=item.get("ai_status_code"),
                    create_time=create_time,
                    remark=item.get("remark"),
                )
            )

        db.add_all(objs)
        db.commit()
        print(f"成功写入 {len(objs)} 条")
        return len(objs)
    except Exception as e:
        db.rollback()
        print(f"写入失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # 测试数据，你可以直接替换成自己的列表
    drop_ai_status_code()
