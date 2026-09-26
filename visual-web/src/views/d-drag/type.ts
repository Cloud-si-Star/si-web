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