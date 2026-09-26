<template>
  <div class="app-page">
    <!-- 路由页面 -->
    <router-view v-slot="{ Component, route }">
      <Transition :name="(route.meta.transition as string) || 'page'" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view>

    <!-- 开门遮罩 -->
    <Transition name="gate" @after-enter="onGateOpened">
      <div v-if="gateVisible" class="gate">
        <div class="gate-door gate-left"  ></div>
        <div class="gate-door gate-right" ></div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const gateVisible = ref(false)

const visual_path='v-visual'

const digital_path='v-digital'

// 路由变化时触发遮罩
watch(
  () => route.path,
  (newPath,oldPath) => {
    if(isNeedTogggle(newPath,oldPath)){
      gateVisible.value = true
    }
  }
)




function isNeedTogggle(newpath:string,oldpath:string):boolean{

  return (newpath.includes(visual_path) && oldpath.includes(digital_path) ) || (newpath.includes(digital_path) && oldpath.includes(visual_path))

}

// 遮罩播放完自动关闭
function onGateOpened() {
  gateVisible.value = false
}
</script>

<style lang="scss" scoped>
.app-page{
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
}

/* ============ 页面过渡（配合遮罩，只做淡入） ============ */


/* ============ 开门遮罩 ============ */
.gate {
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;   /* 不挡点击 */
  overflow: hidden;
}

.gate-door {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  /* 科技感：加一点发光边框 */
  box-shadow: 0 0 40px rgba(64, 158, 255, 0.4);
}


.gate-left {
  left: 0;
  /* 科技感：右边缘一条高亮线 */
  border-right: 2px solid rgba(64, 158, 255, 0.8);
}

.gate-right {
  right: 0;
  border-left: 2px solid rgba(64, 158, 255, 0.8);
}

/* ---------- 遮罩出现（门合上）---------- */
.gate-enter-active {
  transition: opacity 0s ease;
}
.gate-enter-from {
  opacity: 0;
}
.gate-enter-to {
  opacity: 1;
}

/* ---------- 遮罩消失（门滑开）---------- */
.gate-leave-active {
  transition: opacity 0.1s ease 0.6s;   /* 等门滑完再消失 */
}
.gate-leave-to {
  opacity: 0;
}

/* 门滑开动画：用 animation 更可控 */
.gate-leave-active .gate-left {
  animation: slide-left 0.6s cubic-bezier(0.7, 0, 0.3, 1) forwards;
}
.gate-leave-active .gate-right {
  animation: slide-right 0.6s cubic-bezier(0.7, 0, 0.3, 1) forwards;
}

@keyframes slide-left {
  from { transform: translateX(0); }
  to   { transform: translateX(-100%); }
}
@keyframes slide-right {
  from { transform: translateX(0); }
  to   { transform: translateX(100%); }
}
</style>