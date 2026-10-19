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

查看数据库指令
python -m app.scripts.view_database


需求分析
生成模拟数据---》什么样的数据呢
不如以数据决定

这是数据分析师岗位几乎 100% 要求的硬技能。你之前项目里练的窗口函数、CTE、多表 JOIN，方向完全正确。求职时面试官会重点考察：

基础查询（SELECT / WHERE / GROUP BY / HAVING）

多表 JOIN 的逻辑是否清晰

窗口函数（RANK、LAG/LEAD、移动平均）——这是区分“会写 SQL”和“懂分析”的关键

CTE（WITH 子句）拆分复杂查询的能力

你现在的 analysis_service.py 里用 LAG 做环比、用 RANK 做排名、用 CTE 做品类累计占比，这些就是分析师日常最真实的 SQL 场景，继续深挖即可。

```



