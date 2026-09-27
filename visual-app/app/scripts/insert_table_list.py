from datetime import datetime

from app.core.database import SessionLocal
from app.models.ai_info import AiInfo


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
    insert_ai_info(aiTable)
