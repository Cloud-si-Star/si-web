import { ref } from 'vue'
import { chatToApi } from '@/api/chat'

interface Message {
    role: 'user' | 'assistant' | 'system'
    content: string
}

export function useChat() {
    const messages = ref<Message[]>([])
    const aiContent = ref('')
    const isGenerating = ref(false)

    async function sendMessage(userInput: string) {
        if (!userInput.trim() || isGenerating.value) return

        // 添加用户消息
        messages.value.push({ role: 'user', content: userInput })
        aiContent.value = ''
        isGenerating.value = true

        try {


            /*
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: messages.value,
                }),
            })

            */

            const response = await chatToApi.openAiDoor({ messages: messages.value })

            if (!response.ok) throw new Error(`HTTP ${response.status}`)

            const reader = response.body!.getReader()

            const decoder = new TextDecoder('utf-8')

            let buffer = ''

            while (true) {
                const { done, value } = await reader.read()

                if (done) break

                // stream: true 让解码器缓存不完整的多字节字符，避免中文乱码 [citation:12][citation:16]
                buffer += decoder.decode(value, { stream: true })

                // SSE 以 \n\n 分隔事件，最后一段可能不完整，留在 buffer 里
                const lines = buffer.split('\n\n')
                buffer = lines.pop() ?? ''

                for (const line of lines) {
                    if (!line.startsWith('data: ')) continue
                    const data = line.slice(6)

                    if (data === '[DONE]') break
                    if (data.startsWith('[ERROR]')) {
                        aiContent.value += `\n[错误: ${data}]`
                        break
                    }

                    // 后端直接返回纯文本内容，无需 JSON.parse
                    aiContent.value += data
                }
            }

            // 把 AI 回复加入历史，供下一轮对话使用
            messages.value.push({ role: 'assistant', content: aiContent.value })
        } catch (error) {
            console.error('请求失败:', error)
            aiContent.value += '\n[网络请求失败]'
        } finally {
            isGenerating.value = false
        }
    }

    return { messages, aiContent, isGenerating, sendMessage }
}