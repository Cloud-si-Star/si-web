<template>
    <!-- 滚动容器：高度固定为 5 条的高度，超出滚动 -->
    <div ref="containerRef" class="virtual-list" :style="{ height: containerHeight + 'px' }" @scroll.passive="onScroll">
        <!-- 占位容器：撑开总高度，让滚动条长度正确 -->
        <div class="virtual-list__phantom" :style="{ height: totalHeight + 'px' }">
            <!-- 真实渲染的内容，用 translateY 定位到正确位置 -->
            <div class="virtual-list__content" :style="{ transform: `translateY(${offsetY}px)` }">
                <!-- 只渲染可视区的 5 条（+buffer 缓冲） -->
                <div v-for="item in visibleItems" :key="item.id" class="virtual-list__item"
                    :style="{ height: itemHeight + 'px' }">
                    {{ item.name }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Item {
    id: number
    name: string
}

const props = withDefaults(
    defineProps<{
        list: Item[]
        itemHeight?: number
        visibleCount?: number // 可视区固定显示几条
        buffer?: number // 上下各多渲染几条，防止快速滚动露白
    }>(),
    {
        itemHeight: 40,
        visibleCount: 5, // 需求：每次只看见 5 条
        buffer: 2 // 上下各缓冲 2 条，共渲染 5 + 4 = 9 条
    }
)

const { list, itemHeight, visibleCount, buffer } = props

// 容器高度 = 5 条的高度
const containerHeight = computed(() => visibleCount * itemHeight)

// 容器 DOM 引用
const containerRef = ref<HTMLDivElement | null>(null)

// 当前滚动距离
const scrollTop = ref(0)

// 总高度：撑开滚动条
const totalHeight = computed(() => list.length * itemHeight)

// 起始索引：当前滚到第几条，减去 buffer 做上缓冲
const startIndex = computed(() =>
    Math.max(0, Math.floor(scrollTop.value / itemHeight) - buffer)
)

// 结束索引：起始 + 可视 5 条 + 上下 buffer，不能超过总长度
const endIndex = computed(() =>
    Math.min(
        list.length,
        startIndex.value + visibleCount + buffer * 2
    )
)

// 当前实际渲染的数据（永远只有 5 + buffer*2 条）
const visibleItems = computed(() =>
    list.slice(startIndex.value, endIndex.value)
)

// 内容偏移量：把渲染的第一条定位到它在总列表中的位置
const offsetY = computed(() => startIndex.value * itemHeight)

// 用 rAF 节流 scroll 事件，避免高频触发导致卡顿
let ticking = false
function onScroll() {
    if (ticking) return
    ticking = true
    requestAnimationFrame(() => {
        if (containerRef.value) {
            scrollTop.value = containerRef.value.scrollTop
        }
        ticking = false
    })
}
</script>

<style scoped lang="scss">
/* 滚动容器 */
.virtual-list {
    overflow-y: auto;
    border: 1px solid #ddd;
    position: relative;
    width: 400px;
}

/* 占位容器：撑开滚动条总高度 */
.virtual-list__phantom {
    position: relative;
}

/* 真实内容：用 transform 定位 */
.virtual-list__content {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    will-change: transform;
    /* 提示浏览器优化，走 GPU 合成 */
}

/* 单条数据样式 */
.virtual-list__item {
    display: flex;
    align-items: center;
    padding: 0 12px;
    border-bottom: 1px solid #eee;
    box-sizing: border-box;
}
</style>