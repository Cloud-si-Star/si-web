import { request } from '@/utils/request'

/** 菜单类型：0 为未分类/旧默认值，1 为工作台菜单，2 为可视化菜单。 */
export type MenuType = 0 | 1 | 2

/** sys_menu 表对应的菜单记录。 */
export interface MenuItem {
    id: number
    parent_id: number
    label: string
    icon: string
    path: string
    component: string
    sort_order: number
    visible: 0 | 1
    menu_type: MenuType
    created_at: string
    updated_at: string
}

/** 页面树形表格使用的节点结构。 */
export interface MenuTreeNode extends MenuItem {
    children?: MenuTreeNode[]
}

/** 新增菜单请求体；id 与时间戳由数据库生成。 */
export interface CreateMenuDTO {
    parent_id: number
    label: string
    icon: string
    path: string
    component: string
    sort_order: number
    visible: 0 | 1
    menu_type: MenuType
}

/** 菜单可见状态请求体。 */
export interface UpdateMenuVisibilityDTO {
    visible: 0 | 1
}

/**
 * 菜单管理接口。
 * request 会统一剥离后端 { code, message, data } 响应外壳，调用方直接接收 data。
 */
export const menuApi = {
    /** GET /v1/menus：获取由后端按 parent_id 组装好的递归菜单树。 */
    getList() {
        return request.get<MenuTreeNode[]>('/v1/menus')
    },

    /** GET /v1/menus：获取由后端按 parent_id 组装好的递归菜单树。去除parent_id=0的根菜单 */
    getListTree() {
        return request.get<MenuTreeNode[]>('/v1/menus/tree')
    },

    /** POST /v1/menus：创建菜单，成功时返回新建的完整菜单记录。 */
    create(data: CreateMenuDTO) {
        return request.post<MenuItem>('/v1/menus', data)
    },

    /** PATCH /v1/menus/:id/visibility：启用或关闭菜单（修改 visible，不执行物理删除）。 */
    updateVisibility(id: number, data: UpdateMenuVisibilityDTO) {
        return request.patch<MenuItem>(`/v1/menus/${id}/visibility`, data)
    },

    /** DELETE /v1/menus/:id：物理删除菜单；存在子菜单时建议由后端返回冲突错误。 */
    remove(id: number) {
        return request.delete<void>(`/v1/menus/${id}`)
    },
}