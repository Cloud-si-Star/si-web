# visual-app 后端

基于 FastAPI、SQLAlchemy 和 MySQL 的数据可视化平台后端。

## 启动

在仓库根目录执行：

```bash
cd visual-app
uvicorn app.main:app --reload
```

启动前请在 `visual-app/.env` 配置数据库连接参数和 `ERNIE_API_KEY`。API 文档默认可在 `http://127.0.0.1:8000/docs` 查看。

## 目录职责

```text
visual-app/
├── app/
│   ├── api/v1/          # 按资源划分的 HTTP 路由：文件、AI 使用、菜单、对话、销售
│   ├── core/            # 配置、数据库连接和日志等应用基础设施
│   ├── models/          # SQLAlchemy ORM：AI、对话、文件、菜单、销售和 AI 使用分布
│   ├── schemas/         # Pydantic 请求、响应及共享 Schema
│   ├── scripts/         # 数据库操作和演示/种子数据脚本
│   ├── services/        # 业务逻辑、数据库访问和外部模型客户端
│   ├── utils/           # 全局异常处理等通用工具
│   └── main.py          # FastAPI 应用创建、模型注册和 v1 路由装配
├── data/                # 上传文件和样例数据
├── logs/                # 应用运行日志
├── .env                 # 本地环境变量，不提交密钥
└── requirements.txt     # Python 依赖
```

### 代码归类约定

- `api/v1` 只负责 HTTP 参数、状态码、响应格式和调用服务；一个路由模块围绕一个资源或业务域。
- `services` 放业务规则和数据库操作，不依赖 FastAPI 请求对象；外部模型客户端放在 `services/chat_provider.py`。
- `models` 只定义 ORM 表结构；AI 使用分布模型在 `models/ai_usage.py`，销售维度/事实表在 `models/sales.py`。
- `schemas` 定义 API 输入输出，避免路由直接接收无类型的请求体。
- `scripts` 放人工或批量运行的数据准备、数据库维护脚本，不在 API 模块中混放。
- `core/config.py`、`.env`、`requirements.txt` 按本次约定不参与结构迁移；`data/`、`logs/` 和虚拟环境也不是业务源码目录。

## API 路由

接口统一使用 `/api/v1` 前缀。旧 `/api/v2/...` 和 `/api/v1/data/...` 路由已移除；本仓库前端调用已同步更新。

| 方法 | 路径 | 用途 |
|---|---|---|
| `GET` | `/`、`/health` | 基础/详细健康状态 |
| `GET` | `/api/v1/files` | 分页查询文件记录 |
| `POST` | `/api/v1/files` | 上传文件并保存数据库记录 |
| `POST` | `/api/v1/files/content` | 上传文件但不创建数据库记录 |
| `GET` | `/api/v1/files/{file_id}/content` | 下载文件 |
| `GET` | `/api/v1/ai/models` | 分页查询 AI 模型信息 |
| `PATCH` | `/api/v1/ai/models/{ai_id}` | 局部更新 AI 模型信息 |
| `POST` | `/api/v1/ai/usage/distributions` | 批量生成 AI 使用分布数据 |
| `GET` | `/api/v1/ai/usage/provinces` | 按省份汇总使用量 |
| `GET` | `/api/v1/ai/usage/provinces/{province_id}/models` | 查询指定省份各模型使用量 |
| `GET` | `/api/v1/ai/usage/monthly?provinceId=...&aiId=...` | 查询省份/模型的月度使用量 |
| `GET` | `/api/v1/ai/usage/models` | 汇总各模型使用量 |
| `POST` | `/api/v1/ai/provinces` | 写入省份基础数据 |
| `GET` | `/api/v1/menus`、`/api/v1/menus/tree` | 获取完整菜单树 |
| `GET` | `/api/v1/menus/tree/children` | 获取不含顶级菜单节点的子树 |
| `POST` | `/api/v1/menus` | 新建菜单 |
| `PATCH` | `/api/v1/menus/{menu_id}/visibility` | 修改菜单可见状态 |
| `DELETE` | `/api/v1/menus/{menu_id}` | 删除无子菜单的菜单 |
| `GET`、`POST` | `/api/v1/conversations` | 查询/新建会话 |
| `GET` | `/api/v1/conversations/{conversation_id}/messages` | 查询会话消息 |
| `POST` | `/api/v1/conversations/{conversation_id}/messages` | 保存用户消息并以 SSE 流式返回模型答复 |
| `DELETE` | `/api/v1/conversations/{conversation_id}` | 删除会话及其消息 |
| `POST` | `/api/v1/chat/mock` | 不保存会话的 SSE 模型对话 |
| `POST` | `/api/v1/sales/seeds` | 生成销售种子数据 |
| `POST` | `/api/v1/sales/daily-etl?bizdate=YYYYMMDD` | 执行指定日期的销售日汇总 ETL |

上传文件的字段名为 `file`；带记录上传还接受可选的 `upload_user` 和 `remark` 表单字段。AI
对话请求体为 `{ "messages": [{ "role": "user", "content": "..." }] }`。流式接口返回 `text/event-stream`。

## 数据库事务约定

`app/core/database.py` 中有两个不同的 Session 管理方式：

- `get_db()` 用于 `Depends(get_db)`，负责创建和关闭 Session；它本身不统一提交或回滚。
- `get_db_context()` 是上下文管理器，使用 `with` 调用时，代码块正常结束后提交；代码块抛出异常时回滚并继续抛出异常。

需要事务控制的写接口，可以在路由的业务边界使用 `get_db_context()`，并把上下文中的同一个 `db` 传给 service。service
负责业务操作，不自行提交或吞掉异常。示例：

```python
# app/services/record.py
def create_record(db: Session, payload: RecordCreate) -> Record:
    record = Record(**payload.model_dump())
    db.add(record)
    db.flush()  # 在当前事务内执行 SQL；不提交事务
    return record


# app/api/v1/records.py
@router.post("/records")
def create_record_route(payload: RecordCreate):
    with get_db_context() as db:
        record = record_service.create_record(db, payload)
        result = RecordResponse.model_validate(record)

    # 离开 with 后事务已提交；发生异常则已回滚并由异常处理器继续处理
    return success(data=result)
```

上例中的 `Record`、`RecordCreate` 和 `RecordResponse` 代表项目对应的 ORM 模型及 Schema。`db.flush()` 可在不提交事务的情况下执行
SQL 并取得数据库生成的主键；如果 service 不需要这些值，也可以不调用。先在事务块内构造响应 Schema，避免提交并关闭 Session
后再读取过期的 ORM 属性。

不要在这个模式下同时让 service 调用 `db.commit()`；否则 service
提前提交后，外层事务无法回滚已经提交的数据。需要把多个数据库写操作作为一个整体时，让它们共用同一个 `db`
并处于同一个事务块中。`get_db_context()` 只控制数据库事务，不能回滚文件写入、外部 API 调用等非数据库副作用。

现有使用 `Depends(get_db)` 的接口不会自动获得上述事务行为；迁移时需要明确选择事务边界，并移除相应 service
或路由内重复的提交/回滚逻辑。不要在同一条操作链上混用多种事务所有权。

## 数据和运行说明

- 数据库表由模型元数据初始化；正式环境的 schema 变更应使用受控迁移流程，而不是依赖应用启动时自动创建。
- `data/` 中可放样例 CSV 和上传文件；不应将用户上传内容或密钥写进源代码。
- 演示数据生成和数据库维护脚本在 `app/scripts/`，请查看对应脚本说明后再执行；重复运行可能产生重复数据或执行数据修改。

python -m app.scripts.use
