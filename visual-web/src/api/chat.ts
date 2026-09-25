import { request } from '@/utils/request'
import type { PageParams, PageResult } from '@/types/types'

/** chat数据实体 */
interface Message {
    role: 'user' | 'assistant' | 'system'
    content: string
}

/** 更新用户的请求体（全部可选） */
export type UpdateUserDTO = Partial<Message>

/**
 * 用户模块接口
 * 遵循 RESTful：资源用名词，动作用 HTTP 方法表达
 */
export const chatApi_stop = {


    /** POST /users —— 创建用户 */
    openAiDoor(data: any) {
        return request.post('/v2/mock/chat', data)
    }

}

// ✅ 直接用，不需要 import fetch
export const chatApi = {
    async openAiDoor(params: { messages: Message[] }): Promise<Response> {
        return fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params),
        })
    }
}

export const chatToApi = {
    openAiDoor(params: { messages: Message[] }): Promise<Response> {
        return fetch('/api/v2/mock/chat', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        })

    }
}