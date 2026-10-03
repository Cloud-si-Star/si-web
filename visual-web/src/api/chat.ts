import { request } from '@/utils/request'
import type { ApiResponse } from '@/types/types'

/** chat数据实体 */
interface Message {
    role: 'user' | 'assistant' | 'system'
    content: string
}

/** 更新用户的请求体（全部可选） */
export interface NewConversationResponse {
    conversationId: number
    title: string
}

export interface ConversationItem {
    id: number
    title: string
    last_message: string | null
    message_count: number
}

/**
 * 用户模块接口
 * 遵循 RESTful：资源用名词，动作用 HTTP 方法表达
 */
export const chatApi = {
    /* 新增会话使用 */
    addChat() {
        return request.post<NewConversationResponse>('/v1/conversation/new')
    },
    /* 获取会话使用 */
    getChat() {
        return request.get<ConversationItem[]>('/v1/conversation/list')
    },
    /* 获取会话中消息记录所用 */
    getMessage(conversation_id: number) {
        return request.get<Message[]>(`/v1/conversation/${conversation_id}/messages`)
    }
}
