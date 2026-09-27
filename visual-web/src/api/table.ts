import type { PageParams, PageResult, Service‌Response } from "@/types/types"
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

/** 更新用户的请求体（全部可选） */
export type UpdateTableDTO = Partial<tableDTO>

export const tableApi = {

    getList(params: tableListParams) {
        return request.get<PageResult<tableDTO>>('/v1/data/list', params)
    },

    update(params: UpdateTableDTO) {
        return request.patch<Service‌Response>('/v1/data/list', params)
    }

}