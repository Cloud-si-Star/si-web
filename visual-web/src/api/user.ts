import { request } from '@/utils/request'
import type { PageParams, PageResult } from '@/types/types'

/** 用户实体 */
export interface User {
    id: number
    name: string
    email: string
    avatar?: string
}

/** 创建用户的请求体 */
export interface CreateUserDTO {
    name: string
    email: string
    password: string
}

/** 更新用户的请求体（全部可选） */
export type UpdateUserDTO = Partial<CreateUserDTO>

/**
 * 用户模块接口
 * 遵循 RESTful：资源用名词，动作用 HTTP 方法表达
 */
export const userApi = {
    /** GET /users —— 获取用户列表（分页） */
    getList(params: PageParams) {
        return request.get<PageResult<User>>('/v1/data/files')
    },

    /** GET /users/:id —— 获取单个用户 */
    getById(id: number) {
        return request.get<User>(`/users/${id}`)
    },

    /** POST /users —— 创建用户 */
    create(data: CreateUserDTO) {
        return request.post<User>('/users', data)
    },

    /** PUT /users/:id —— 全量更新用户 */
    update(id: number, data: UpdateUserDTO) {
        return request.put<User>(`/users/${id}`, data)
    },

    /** PATCH /users/:id —— 局部更新用户 */
    patch(id: number, data: UpdateUserDTO) {
        return request.patch<User>(`/users/${id}`, data)
    },

    /** DELETE /users/:id —— 删除用户 */
    remove(id: number) {
        return request.delete<void>(`/users/${id}`)
    },
}