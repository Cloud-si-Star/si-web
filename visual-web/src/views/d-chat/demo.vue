<template>
    <div class="con-page">
        <div class="nav-page">

        </div>

        <div>

        </div>
    </div>
</template>


<script setup lang="ts">
import { useChat } from './index';
import { ref, watch,nextTick } from 'vue';

const {messages,aiContent,isGenerating,sendMessage} = useChat()

const input = ref('')
const listRef = ref<HTMLElement |null >(null)

async function handleSend(){
    const text=input.value.trim()

    if(!text ||isGenerating.value) return

    input.value=''

    await sendMessage(text)

    scrollToBottom()
}

function scrollToBottom(){
    nextTick(()=>{
        if(listRef.value){
            listRef.value.scrollTop = listRef.value.scrollHeight
        }
    })
}


watch(aiContent,scrollToBottom)
</script>