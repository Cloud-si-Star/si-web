<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'

interface Props {
  /** 边框主色，默认青蓝 */
  color?: string
  /** 流动光带颜色（高亮），默认亮青 */
  lightColor?: string
  /** 边框粗细 */
  strokeWidth?: number
  /** 圆角半径 */
  radius?: number
  /** 流动动画时长（秒） */
  duration?: number
  /** 标题文字，不传则不显示 */
  title?: string
  /** 标题位置：top-left | top-center | top-right */
  titlePosition?: 'top-left' | 'top-center' | 'top-right'
  /** 是否显示流动动画 */
  animated?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  color: '#0891b2',
  lightColor: '#00e5ff',
  strokeWidth: 1.5,
  radius: 5,
  duration: 3,
  title: 'rangw see you',
  titlePosition: 'top-left',
  animated: true,
})

/** 每个实例用独立 id，避免多组件时 SVG defs 冲突 */
const uid = `svg-border-${Math.random().toString(36).slice(2, 9)}`
const gradientId = `${uid}-gradient`
const glowId = `${uid}-glow`

const wrapRef = ref<HTMLElement | null>(null)

/** 计算路径：圆角矩形的 path d（用 100x100 viewBox + preserveAspectRatio=none 自适应） */
const pathD = computed(() => {
  const r = props.radius
  // 用百分比坐标，viewBox 100x100，preserveAspectRatio="none" 会拉伸
  // 但圆角会被拉伸变形，所以改用 1000x1000 + 矢量不变形方案见下方说明
  return `M ${r} 0 H ${100 - r} A ${r} ${r} 0 0 1 100 ${r} V ${100 - r} A ${r} ${r} 0 0 1 ${100 - r} 100 H ${r} A ${r} ${r} 0 0 1 0 ${100 - r} V ${r} A ${r} ${r} 0 0 1 ${r} 0 Z`
})

/** 标题位置样式 */
const titleStyle = computed(() => {
  const pos = props.titlePosition
  if (pos === 'top-center') return { left: '50%', transform: 'translateX(-50%)' }
  if (pos === 'top-right') return { right: '16px' }
  return { left: '16px' }
})

/** 描边动画：dasharray 控制虚线段长度，dashoffset 滚动 */
const dashArray = computed(() => {
  // 光带长度 = 周长的百分比；这里用固定值，配合 dashoffset 动画
  return '60 240'
})

defineExpose({
  /** 暴露容器，方便父组件做 resize 等 */
  getEl: () => wrapRef.value,
})
</script>

<template>
  <div
    ref="wrapRef"
    class="svg-border"
    :style="{
      '--sb-color': color,
      '--sb-light': lightColor,
      '--sb-stroke': strokeWidth + 'px',
      '--sb-radius': radius + 'px',
      '--sb-duration': duration + 's',
    }"
  >
    <!-- SVG 边框层 -->
    <svg
      class="svg-border__svg"
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <defs>
        <!-- 渐变：青蓝色系 -->
        <linearGradient :id="gradientId" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="color" />
          <stop offset="50%" :stop-color="lightColor" />
          <stop offset="100%" :stop-color="color" />
        </linearGradient>

        <!-- 发光滤镜 -->
        <filter :id="glowId" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="1.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <!-- 底框：静态细线 -->
      <path
        :d="pathD"
        fill="none"
        :stroke="color"
        :stroke-width="strokeWidth * 0.6"
        :stroke-opacity="0.35"
        vector-effect="non-scaling-stroke"
      />

      <!-- 流动光带 -->
      <path
        v-if="animated"
        class="svg-border__flow"
        :d="pathD"
        fill="none"
        :stroke="`url(#${gradientId})`"
        :stroke-width="strokeWidth"
        :stroke-dasharray="dashArray"
        :filter="`url(#${glowId})`"
        stroke-linecap="round"
        vector-effect="non-scaling-stroke"
      />
    </svg>

    <!-- 标题：绝对定位在顶部边框上 -->
    <div
      v-if="title"
      class="svg-border__title"
      :style="titleStyle"
    >
      {{ title }}
    </div>

    <!-- 内容区：接收 div / 图表 -->
    <div class="svg-border__content">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.svg-border {
  // 宽高继承父级
  position: relative;
  width: 100%;
  height: 100%;
  box-sizing: border-box;

  // 内容与边框留点间距
  padding: 5px;

  // SVG 层
  &__svg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: visible;
  }

  // 流动光带
  &__flow {
    stroke-dashoffset: 0;
    animation: svg-border-flow var(--sb-duration, 3s) linear infinite;
  }

  // 标题
  &__title {
    position: absolute;
    top: 0;
    transform: translateY(-50%);
    padding: 0 8px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1px;
    color: var(--sb-light, #00e5ff);
    background: var(--sb-title-bg, #0b1220); // 盖住边框线
    text-shadow: 0 0 6px var(--sb-light, #00e5ff);
    white-space: nowrap;
    pointer-events: none;
    z-index: 1;
  }

  // 内容区
  &__content {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  // 减少动画偏好
  @media (prefers-reduced-motion: reduce) {
    &__flow {
      animation: none;
    }
  }
}

@keyframes svg-border-flow {
  to {
    stroke-dashoffset: -300; // = dasharray 总长，形成无缝循环
  }
}
</style>