<script setup lang="ts">
interface Props {
    width?: number | string
    height?: number | string
    color?: string
    glow?: boolean
    glowIntensity?: number
}

withDefaults(defineProps<Props>(), {
    width: 36,
    height: 36,
    color: '#1677ff',
    glow: true,
    glowIntensity: 0.6,
})
</script>

<template>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" :width="width" :height="height"
        aria-label="数智可视化工作台系统 Logo" role="img">
        <defs>
            <!-- 主渐变：蓝紫青 -->
            <linearGradient id="logoGradient" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#1e5bff" />
                <stop offset="45%" stop-color="#0ea5e9" />
                <stop offset="100%" stop-color="#22d3ee" />
            </linearGradient>

            <!-- 柱状图渐变：青蓝紫 -->
            <linearGradient id="barGradient" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stop-color="#22d3ee" />
                <stop offset="60%" stop-color="#0ea5e9" />
                <stop offset="100%" stop-color="#6366f1" />
            </linearGradient>

            <!-- 局部高光 -->
            <linearGradient id="highlightGradient" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="0.55" />
                <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
            </linearGradient>

            <!-- 发光滤镜：只在开启时生效 -->
            <filter id="softGlow" v-if="glow">
                <feGaussianBlur std-deviation="4" result="blur" />
                <feColorMatrix in="blur" type="matrix"
                    :values="`1 0 0 0 0.12  0 1 0 0 0.35  0 0 1 0 0.93  0 0 0 ${glowIntensity} 0`" result="glow" />
                <feMerge>
                    <feMergeNode in="glow" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>
        </defs>

        <g :filter="glow ? 'url(#softGlow)' : undefined">
            <!-- 外层圆环 -->
            <circle cx="64" cy="64" r="54" fill="none" stroke="url(#logoGradient)" stroke-width="6" />

            <!-- 内层圆环 -->
            <circle cx="64" cy="64" r="44" fill="none" stroke="url(#logoGradient)" stroke-width="2" opacity="0.85" />

            <!-- 屏幕外框：纤薄圆润悬浮面板 -->
            <rect x="34" y="42" width="60" height="44" rx="10" ry="10" fill="#ffffff" stroke="url(#logoGradient)"
                stroke-width="2.5" />

            <!-- 屏幕内部柱状图 -->
            <g transform="translate(44, 54)">
                <rect x="0" y="18" width="8" height="6" rx="1.5" fill="url(#barGradient)" />
                <rect x="14" y="12" width="8" height="12" rx="1.5" fill="url(#barGradient)" />
                <rect x="28" y="4" width="8" height="20" rx="1.5" fill="url(#barGradient)" />
                <line x1="0" y1="24" x2="36" y2="24" stroke="#0ea5e9" stroke-width="1" opacity="0.6" />
            </g>

            <!-- 屏幕高光 -->
            <rect x="34" y="42" width="60" height="10" rx="10" fill="url(#highlightGradient)" opacity="0.5" />

            <!-- 右下装饰弧 -->
            <path d="M92 92 C100 86 106 76 108 64" fill="none" stroke="#22d3ee" stroke-width="3" opacity="0.75" />
        </g>
    </svg>
</template>
