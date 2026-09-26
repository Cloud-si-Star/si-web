<template>
  <div class="con-page">
    <div class="nav-page"></div>
    <div class="chat-container">
      <!-- 消息列表 -->
      <div class="message-list" ref="listRef">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
         
          <Avatar :type="msg.role==='user'?'user':'ai'"></Avatar>
          <div class="bubble">{{ msg.content }}</div>
        </div>

        <!-- 正在生成的 AI 回复 -->
        <div v-if="isGenerating" class="message assistant">
          <Avatar type="ai"></Avatar>
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
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { useChat } from './index.ts'
import Avatar from '@/components/Avatar.vue'

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

<style scoped lang="scss">
.nav-page{
  width: 160px;
  height: 100%;
  border: 1px solid #EEE;
}


.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
  margin: 10px;
  background: #f3f3ff;
  border-radius: 5px;
  box-sizing: border-box;
  overflow: hidden;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  &::-webkit-scrollbar {
    width: 8px;
  }
  &::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(52, 145, 233, 0.45);
    border-radius:4px;
    &:hover{
      background: rgba(25, 142, 252, 0.75);
    }
  }
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
  background-color: #43cee9;
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