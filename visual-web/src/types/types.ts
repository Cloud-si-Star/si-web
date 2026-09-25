/* 后端统一约定响应体 */
export interface ApiResponse<T = unknown> {
    code: number,
    message: string
    data: T
}


/* 约定分页请求参数 */
export interface PageParams {
    page: number,
    pageSize: number
}

/* 分页响应结构 */
export interface PageResult<T> {
    list: T[],
    total: number,
    page: number,
    pageSize: number
}