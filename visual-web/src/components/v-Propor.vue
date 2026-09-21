<template>
  <div 
    class="rank-container"
    @mouseenter="pauseTask"
    @mouseleave="startTask"
  >
    <div class="rank-wrap" :style="{transform: `translateY(-${offset}px)`}">
      <div class="rank-list">
        <div class="rank-item" v-for="item in list" :key="item.id">
          <span class="rank-no">No.{{item.rank}}</span>
          <span class="rank-name">{{item.name}}</span>
          <div class="bar-bg">
            <div class="bar-fill" :style="{width: (item.value / maxVal *100)+'%'}"></div>
          </div>
          <span class="rank-num">{{item.value}}</span>
        </div>
      </div>
      <div class="rank-list">
        <div class="rank-item" v-for="item in list" :key="item.id + 'copy'">
          <span class="rank-no">No.{{item.rank}}</span>
          <span class="rank-name">{{item.name}}</span>
          <div class="bar-bg">
            <div class="bar-fill" :style="{width: (item.value / maxVal *100)+'%'}"></div>
          </div>
          <span class="rank-num">{{item.value}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, onMounted, onUnmounted, watch} from 'vue'
interface RankItem {
  id: number
  rank: number
  name: string
  value: number
}
const list = ref<RankItem[]>([
  {id:1, rank:3, name:'周口',value:55},
  {id:2, rank:4, name:'信阳',value:45},
  {id:3, rank:5, name:'漯河',value:29},
  {id:4, rank:1, name:'南阳',value:120},
  {id:5, rank:2, name:'新乡',value:80},
])
const maxVal = computed(()=> Math.max(...list.value.map(i=>i.value)))

const offset = ref(0)
const itemHeight = 44
const totalHeight = computed(()=> list.value.length * itemHeight)

let rafId: number | null = null
let isRunning = ref(false)

// 【任务：开始滚动】
const startTask = () => {
  if(isRunning.value) return
  isRunning.value = true
  function animate() {
    offset.value += 0.6
    if(offset.value >= totalHeight.value) {
      offset.value = 0
    }
    rafId = requestAnimationFrame(animate)
  }
  rafId = requestAnimationFrame(animate)
}
// 【任务：暂停滚动】
const pauseTask = () => {
  isRunning.value = false
  if(rafId) {
    cancelAnimationFrame(rafId)
    rafId = null
  }
}

// 监听数据变化：数据刷新 → 重置滚动任务
watch(list, ()=>{
  offset.value = 0
  pauseTask()
  startTask()
}, {deep:true})

onMounted(()=>{
  startTask()
  // 页面切tab，自动暂停
  document.addEventListener('visibilitychange', ()=>{
    if(document.hidden) pauseTask()
    else startTask()
  })
})
onUnmounted(()=>{
  pauseTask() // 销毁任务，释放资源
})
</script>

<style scoped>
.rank-container{
  width:100%;
  height:320px;
  overflow:hidden;
  background: rgba(77, 95, 255, 0.12);
  padding:16px;
  border-radius:6px;
}
.rank-wrap{
  width:100%;
}
.rank-item{
  height:44px;
  display:flex;
  align-items:center;
  gap:12px;
  color:#fff;
}
.rank-no{
  color:#40b8ff;
  width:60px;
}
.rank-name{
  width:60px;
}
.bar-bg{
  flex:1;
  height:5px;
  background:rgba(64,224,208,0.15);
  border-radius:3px;
}
.bar-fill{
  height:100%;
  border-radius:3px;
  background: linear-gradient(90deg, #40e0d0, #36c9ff);
}
.rank-num{
  width:40px;
  text-align:right;
}
</style>
