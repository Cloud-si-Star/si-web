import { ref } from "vue"

interface Message {
    role: 'user' | 'assistant' | 'system',
    content: string
}

function chatToAiWorld(params: { messages: Message[] }): Promise<Response> {
    return fetch('/api/v2/mock/chat', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(params)
    })
}

export function useChat() {
    const messages = ref<Message[]>([])
    const aiContent = ref('')
    const isGenerating = ref(false)

    async function sendMessage(userInput: string) {
        if (!userInput.trim() || isGenerating.value) return
        messages.value.push(
            {
                role: 'user',
                content: userInput.trim()
            }
        )

        aiContent.value = ''
        isGenerating.value = true

        try {
            const response = await chatToAiWorld({ messages: messages.value })

            if (!response.ok) throw new Error(`HTTP ${response.status}`)

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
                    const data = line.slice(6)

                    if (data === '[DONE]') break

                    if (data.startsWith('[ERROR]')) {
                        aiContent.value += `\n[错误: ${data}]`
                        break
                    }

                    aiContent.value += data

                }
            }
            messages.value.push({
                role: 'assistant',
                content: aiContent.value
            })
        } catch (error) {
            console.log('请求失败: ', error)
            aiContent.value += '\n[网络请求失败]'
        } finally {
            isGenerating.value = false
        }
    }

    return { aiContent, isGenerating, messages, sendMessage }
}