import { ref } from "vue"

export interface Message {
    role: 'user' | 'assistant' | 'system'
    content: string
}

function chatAiToWorld(params: { conversation_id: number, messages: Message[] }): Promise<Response> {
    return fetch('/api/v2/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
}

export const chatApi = () => {
    const messages = ref<Message[]>([])
    const aiContent = ref('')
    const isGenerating = ref(false)

    async function sendMessage(userInput: string, conversation_id: number) {
        if (!userInput.trim() || isGenerating.value) return

        aiContent.value = ''
        isGenerating.value = true

        try {
            const response = await chatAiToWorld({ conversation_id: conversation_id, messages: messages.value })

            if (!response.ok) throw new Error(`请求错误：${response.status}`)

            const reader = response.body!.getReader()

            const decoder = new TextDecoder('utf-8')

            messages.value.push({ role: 'user', content: userInput.trim() })

            let buffer = ''

            while (true) {
                const { done, value } = await reader?.read()

                if (done) break

                buffer += decoder.decode(value, { stream: true })

                const lines = buffer.split('\n\n')

                buffer = lines.pop() ?? ''

                for (const line of lines) {
                    if (!line.startsWith('data: ')) continue

                    let text = line.slice(6)

                    if (text.startsWith('[DONE]')) break

                    if (text.startsWith('[ERROR}')) {
                        aiContent.value += '【错误】' + text
                        break
                    }

                    aiContent.value += text
                }

            }

            messages.value.push({ role: 'assistant', content: aiContent.value })

        } catch (error) {
            console.log('请求错误:', error);
            aiContent.value += `【错误】：${error}`
        } finally {
            isGenerating.value = false
        }


    }

    return { messages, aiContent, isGenerating, sendMessage }
}


export function debounce(fn: (...args: any[]) => {}, delay: number) {
    let timer: number | null = null
    return (...args: any[]) => {
        if (timer) clearTimeout(timer)
        timer = window.setTimeout(() => {
            fn(...args)
        }, delay)
    }
}