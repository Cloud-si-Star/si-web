import type { PageParams, PageResult } from "@/types/types"
import { request } from "@/utils/request"

/* 创建用户的请求体 */
export interface searchForm {
    ai_name: string
    use_date: string
    ai_status: string
}

export interface tableDTO {
    ai_id: number
    ai_name: string
    ai_status: string
    ai_use: number
    create_time: string
    remark: string
}

export interface tableListParams extends PageParams, searchForm { }


export const tableApi = {

    getList(params: tableListParams) {
        return request.get<PageResult<tableDTO>>('/v1/data/list', params)
    }
}