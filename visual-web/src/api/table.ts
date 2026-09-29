import type { PageParams, PageResult, Service‌Response, ApiResponse } from "@/types/types"
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

const arrName = ['张无忌', '赵敏', '周芷若', '小龙女', '郭襄', '黄蓉', '任盈盈', '王语嫣', '阿朱', '阿紫']

/** 更新用户的请求体（全部可选） */
export type UpdateTableDTO = Partial<tableDTO>

export const tableApi = {

    getList(params: tableListParams) {
        return request.get<PageResult<tableDTO>>('/v1/data/list', params)
    },

    update(params: UpdateTableDTO) {
        return request.patch<Service‌Response>('/v1/data/list', params)
    },

    upload(params: File) {
        let cfg = {
            headers: { 'Content-Type': 'multipart/form-data' }
        }

        const formData = new FormData()

        formData.append('file', params)

        /* 从arrName中随机取一个名字作为上传用户 */
        const randomName = arrName[Math.floor(Math.random() * arrName.length)]

        formData.append('upload_user', randomName!)

        formData.append('remark', '测试文件')

        return request.post<ApiResponse>('/v1/data/with-record', formData, cfg)
    }

}
