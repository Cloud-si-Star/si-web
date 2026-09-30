# 菜单管理后端接口协作清单

前端调用 `src/api/menu.ts`，Axios 使用 `VITE_API_BASE_URL` 作为配置的 baseURL，并将统一响应 `{ code, message, data }` 解包为 `data`。要与当前后端路径匹配，baseURL 应配置为服务地址加 `/api`（例如 `http://localhost:8000/api`）；后端 v1 路由前缀为 `/api/v1`。

| 功能 | 方法与路径 | 请求 | `data` 响应 | 后端协作要求 |
| --- | --- | --- | --- | --- |
| 查询菜单列表 | `GET /api/v1/menus` | 无 | `MenuTreeItem[]`，后端按 `parent_id` 返回递归 `children` 树 | 每层按 `sort_order ASC, id ASC` 排序；无父记录的菜单作为根节点返回；字段名使用 SQL 下划线形式 |
| 新增菜单 | `POST /api/v1/menus` | `CreateMenuDTO` JSON | 新建后的完整 `MenuItem` | 校验必填字段及父级菜单存在；`id`、`created_at`、`updated_at` 由数据库生成 |
| 启用/关闭菜单 | `PATCH /api/v1/menus/{id}/visibility` | `{ "visible": 0 }` 或 `{ "visible": 1 }` | 更新后的完整 `MenuItem` | `visible=0` 为关闭，`visible=1` 为启用；该操作保留记录，不是删除 |
| 删除菜单 | `DELETE /api/v1/menus/{id}` | 无 | `null` 或成功标记 | 物理删除；存在子菜单时返回 HTTP 409，避免孤儿记录；不存在返回 HTTP 404 |

## 字段类型

```ts
interface MenuTreeItem {
  id: number
  parent_id: number
  label: string
  icon: string
  path: string
  component: string
  sort_order: number
  visible: 0 | 1
  menu_type: 0 | 1 | 2
  created_at: string
  updated_at: string
  children: MenuTreeItem[]
}

interface CreateMenuDTO {
  parent_id: number // 0 表示顶级菜单
  label: string
  icon: string
  path: string
  component: string
  sort_order: number
  visible: 0 | 1
  menu_type: 1 | 2 // 1 工作台，2 可视化；数据库默认 0 供旧记录兼容
}
```

## 响应与错误约定

成功响应沿用项目统一结构，例如：

```json
{
  "code": 0,
  "message": "success",
  "data": []
}
```

推荐参数错误返回 HTTP 422 或 400，未找到返回 404，删除有子菜单返回 409；错误正文提供可读的 `detail` 或项目统一错误字段，前端 Axios 拦截器会将错误转成提示消息。

## 表结构注意事项

`sys_menu` 当前没有软删除字段，因此关闭菜单只修改 `visible`；删除接口是不可恢复的物理删除。列表接口由后端组装树形结构，前端直接使用 `children` 展示，不再按 `parent_id` 自行构树。
