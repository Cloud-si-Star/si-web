<template>
    <div class="layout-wrap">
        <div class="fixed-open" @click="handleMenu" :class="{ isActive: isOpen }">

            <Transition mode="out-in">
                <el-icon v-if="isOpen" key="expand">
                    <Expand />
                </el-icon>
                <el-icon v-else key="fold">
                    <Fold />
                </el-icon>
            </Transition>

        </div>
        <!-- 左侧菜单栏 -->
        <visualMenu :isOpen="isOpen"></visualMenu>

        <!-- 右侧：子页面渲染位置！！子路由全部渲染在这里 -->
        <main class="main-content">
            <router-view v-slot="{ Component }">
                <!-- 路由切换动画 -->
                <transition name="fade" mode="out-in">
                    <!-- keep-alive 缓存页面，对应你之前路由不销毁的特性 -->
                    <!-- Component 由 router-view 自动注入，路由变它自动变 -->
                    <component :is="Component" />
                </transition>
            </router-view>
        </main>
    </div>
</template>

<script setup lang="ts">
import visualMenu from './visual-menu.vue'
import { onUnmounted, ref } from 'vue'

/* ==========菜单滑动滑出========== */

const isOpen = ref<boolean>(true)
const handleMenu = () => {
    isOpen.value = !isOpen.value
}



</script>

<style scoped lang="scss">
.layout-wrap {
    display: flex;
    height: 100%;
    box-sizing: border-box;
}

.main-content {
    flex: 1;
    background: #f5f7fa;
    overflow: auto;
    box-sizing: border-box;
}

.fixed-open {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 999;
    color: rgb(79 195 255 / 60%);
    font-size: 35px;
    box-sizing: border-box;
    transition: transform 1s ease;

    &:hover {
        color: #60f1e7;
        cursor: pointer;
    }
}

.isActive {
    transform: translate(170px, 0px);
}
</style>