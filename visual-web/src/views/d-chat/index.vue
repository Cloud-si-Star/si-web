<template>
  <div class="chat-container">
    <!-- 消息列表 -->
    <div class="message-list" ref="listRef">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="avatar">{{ msg.role === 'user' ? '我' : 'AI' }}</div>
        <div class="bubble">{{ msg.content }}</div>
      </div>

      <!-- 正在生成的 AI 回复 -->
      <div v-if="isGenerating" class="message assistant">
        <div class="avatar">AI</div>
        <div class="bubble">
          {{ aiContent }}
          <span class="cursor">▊</span>
        </div>
      </div>
    </div>

    <!-- 输入区 -->
    <div class="input-area">
      <textarea
        v-model="input"
        placeholder="输入消息，Enter 发送，Shift+Enter 换行"
        @keydown.enter.exact.prevent="handleSend"
        :disabled="isGenerating"
        rows="2"
      />
      <button @click="handleSend" :disabled="isGenerating || !input.trim()">
        {{ isGenerating ? '生成中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { useChat } from './chat.ts'

const { messages, aiContent, isGenerating, sendMessage } = useChat()

const input = ref('')
const listRef = ref<HTMLElement | null>(null)

async function handleSend() {
  const text = input.value.trim()
  if (!text || isGenerating.value) return

  input.value = ''
  await sendMessage(text)
  scrollToBottom()
}

function scrollToBottom() {
  nextTick(() => {
    if (listRef.value) {
      listRef.value.scrollTop = listRef.value.scrollHeight
    }
  })
}

// 流式输出时自动滚到底部
watch(aiContent, scrollToBottom)
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  background: #f7f7f8;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  display: flex;
  gap: 10px;
  margin-bottom: 18px;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
  background: #e5e5e5;
}

.message.user .avatar {
  background: #4a90e2;
  color: #fff;
}

.bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 10px;
  background: #fff;
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
}

.message.user .bubble {
  background: #4a90e2;
  color: #fff;
}

.cursor {
  animation: blink 1s step-start infinite;
  color: #4a90e2;
}

@keyframes blink {
  50% { opacity: 0; }
}

.input-area {
  display: flex;
  gap: 10px;
  padding: 16px;
  background: #fff;
  border-top: 1px solid #e5e5e5;
}

textarea {
  flex: 1;
  resize: none;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
}

textarea:focus {
  border-color: #4a90e2;
}

button {
  padding: 0 24px;
  border: none;
  border-radius: 8px;
  background: #4a90e2;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover:not(:disabled) {
  background: #357abd;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>