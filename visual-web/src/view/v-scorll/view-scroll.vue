<template>
  <div class="page">
    <div class="left-wrap">
      <!-- 夹点按钮：像 Dock / 垃圾桶 -->
      <button class="pin-btn" @click="startMinimize" ref="btnRef">
        <span class="pin-icon"></span>
      </button>

      <!-- 要被最小化的 div -->
      <div
        ref="targetRef"
        class="target-box"
        :class="{ minimizing: isMinimizing }"
      >
        <div class="content">帕子内容</div>
      </div>
    </div>

    <div class="right-box">
      右侧自动占据空间
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const targetRef = ref<HTMLDivElement | null>(null)

const isMinimizing =ref<boolean>(false)

function startMinimize(){
    isMinimizing.value=!isMinimizing.value
}



</script>

<style scoped lang="scss">
.page {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
  height: 420px;
  background: #f5f7fa;
  padding: 24px;
  box-sizing: border-box;
}

.left-wrap {
  position: relative;
  width: 320px;
  height: 100%;

  /* 左侧宽度平滑收缩 */
  transition: width 0.6s cubic-bezier(0.65, 0, 0.35, 1);
  flex-shrink: 0;
}

/* 夹点按钮：模拟被吸入的目标点 */
.pin-btn {
  position: absolute;
  top: -14px;
  left: -14px;
  z-index: 30;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: #409eff;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(64, 158, 255, 0.45);

  display: flex;
  align-items: center;
  justify-content: center;
}

.pin-icon {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #fff;
  box-shadow: inset 0 0 0 3px #409eff;
}

/* 被最小化的 div */
.target-box {
  width: 100%;
  height: 100%;
  background: linear-gradient(145deg, #ffe58f, #ffd54f);
  border-radius: 12px;
  border-top-left-radius: 0px;
  
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);

  display: flex;
  align-items: center;
  justify-content: center;

  /* 动画原点在左上角按钮附近 */
  transform-origin: top left;

  transition:
    transform 0.5s cubic-bezier(0.5, 0, 0.2, 1.2),
    opacity 0.45s ease-in,
    border-radius 0.4s,
    box-shadow 0.4s;
}

.content {
  color: #5c4a12;
  font-size: 16px;
  font-weight: 500;
}

/* 关键：模拟 macOS 最小化的吸入动画 */
.target-box.minimizing {
  /* 向夹点方向大幅缩小，而不是平移飞走 */
  transform:
    translate(-6%, -6%)
    scale(0.12);

  opacity: 0;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  pointer-events: none;
}

/* 左侧容器宽度收窄，右侧自动补位 */
.left-wrap:has(.minimizing) {
  width: 0;
}

/* 右侧 div 平滑扩张 */
.right-box {
  flex: 1;
  height: 100%;
  background: linear-gradient(145deg, #95de64, #67c243);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2b4d14;
  font-size: 16px;
  font-weight: 500;

  transition: flex 0.6s cubic-bezier(0.65, 0, 0.35, 1);
}
</style>
