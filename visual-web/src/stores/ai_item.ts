import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ai_item {
    ai_id: number
    ai_name: string
    ai_use: number
}

const ai_arr: ai_item[] = [
    { ai_id: 52817, ai_name: 'DeepSeek', ai_use: 892341 },
    { ai_id: 31204, ai_name: 'ChatGPT', ai_use: 1523876 },
    { ai_id: 74619, ai_name: 'Claude', ai_use: 734219 },
    { ai_id: 19083, ai_name: 'Gemini', ai_use: 612874 },
    { ai_id: 60527, ai_name: '文心一言', ai_use: 458123 },
    { ai_id: 28451, ai_name: '通义千问', ai_use: 392640 },
    { ai_id: 93716, ai_name: 'Kimi', ai_use: 351208 },
    { ai_id: 46182, ai_name: '豆包', ai_use: 287495 },
    { ai_id: 82035, ai_name: 'Copilot', ai_use: 245671 },
    { ai_id: 17394, ai_name: 'Grok', ai_use: 198320 }
]

export const useAiStore = defineStore('ai-use', () => {
    const aiTable = ref<ai_item[]>(ai_arr)

    /* 业务逻辑 获取表格数据 */
    const getAiTable = () => aiTable.value
    /* 业务逻辑 添加使用数据 */
    const addAiItem = (param: ai_item) => {
        for (let key of aiTable.value) {
            if (key.ai_id == param.ai_id) {
                key.ai_use += param.ai_use
                break
            }
        }

    }

    return { aiTable, getAiTable, addAiItem }
})