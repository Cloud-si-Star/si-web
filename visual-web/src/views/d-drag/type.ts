import { request } from "@/utils/request"
/* 定义搜索实体 */
export interface searchForm {
    ai_name: string
    use_date: [string, string] | []
    ai_status: string
}

export interface tableDTO {
    ai_id: number,
    ai_name: string,
    ai_status: string,
    ai_use: number,
    create_time: [],
    remark: string
}

export const boardApi = {
    /* 造数据 */
    faker_sql_data() {
        return request.get('/v1/sales/batch')
    }
}

