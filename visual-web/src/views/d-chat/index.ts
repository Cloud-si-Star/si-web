import { ref } from "vue"

export interface Message {
    role: 'user' | 'assistant' | 'system'
    content: string
}

/**
 * 
 * @param  message类型传递给后端模型数据
 * @returns 
 */
function chatAiWorld(params: { conversation_id: number, messages: Message[] }): Promise<Response> {
    return fetch('/api/v2/chat', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(params)
    })
}

/**
 * 定义对象 里面有sendmessage方法请求接口  处理数据
 */
export const useChat = () => {
    const messages = ref<Message[]>([])
    const aiContent = ref('')
    const isGenerating = ref(false)

    async function sendMessage(userInput: string, conversation_id: number) {
        /* 用户输入为空 或者 正在生成中 都不执行方法 */
        if (!userInput.trim() || isGenerating.value) return

        isGenerating.value = true

        aiContent.value = ''

        messages.value.push({ role: 'user', content: userInput.trim() })

        try {

            const response = await chatAiWorld({ conversation_id: conversation_id, messages: messages.value })

            if (!response.ok) throw new Error(`HTTP ERROR ${response.status}`)

            const reader = response.body!.getReader()

            const decoder = new TextDecoder('utf-8')

            let buffer = ''

            while (true) {
                const { done, value } = await reader.read()

                if (done) break

                buffer += decoder.decode(value, { stream: true })

                const lines = buffer.split('\n\n')

                buffer = lines.pop() ?? ''

                for (const line of lines) {
                    if (!line.startsWith('data: ')) continue
                    /* 因为格式就是第六个之后才是内容 约定 */
                    let text = line.slice(6)

                    if (text == '[DONE]') break

                    if (text.startsWith('[ERROR]')) {
                        aiContent.value += `\n[错误: ${text}]`
                        break
                    }

                    aiContent.value += text

                }
            }

            messages.value.push({ role: 'assistant', content: aiContent.value })

        } catch (error) {
            console.error('请求失败:', error)
            aiContent.value += '\n[网络请求失败]'
        } finally {
            isGenerating.value = false
        }

    }
    return { messages, aiContent, sendMessage, isGenerating }
}