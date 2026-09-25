# window-ae FastAPI 项目

## 启动
```bash
cd /Users/luosi-8937/Desktop/AIIDE/window-ae
uvicorn app.main:app --reload
```

## 接口
- `GET /`                            健康检查
- `GET /api/v1/data/files`           列出 data 目录下的 csv 文件
- `GET /api/v1/data/csv/{filename}`  读取指定 csv 内容

## 说明
把要读取的 csv 放到 `data/` 目录下（已放入示例 `clicks.csv`），
然后访问 `http://127.0.0.1:8000/api/v1/data/csv/clicks.csv` 即可拿到数据。

## 目录结构
```
window-ae/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── core/config.py       # 配置
│   ├── schemas/response.py  # 统一响应体
│   ├── api/v1/data.py       # CSV 数据接口
│   ├── services/csv_service.py  # CSV 读取逻辑
│   └── utils/exceptions.py  # 全局异常处理
├── data/                    # csv 数据目录
├── requirements.txt
└── README.md
```



