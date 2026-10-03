<template>
    <div class="logo-box">
        <vlogo></vlogo>
        <div style="display: flex;">
            <span>数智</span>
            <span class="type-active">{{ title }}
                <el-icon size="18" class="icon-active" @click="go">
                    <Switch />
                </el-icon>
            </span>

        </div>
    </div>
</template>

<script setup lang="ts">
import vlogo from '@/components/v-logo.vue'
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const path = {
    visual: '/v-visual',
    digital: '/d-digital'
}

const route = useRoute()

const router = useRouter()

const title = computed(() => {
    return route.path.includes(path.visual) ? '可视化' : '工作台'
})

const go = () => {
    if (route.path.includes(path.visual)) {
        router.push(path.digital)
    } else {
        router.push(path.visual)
    }
}


</script>

<style lang="scss" scoped>
.logo-box {
    display: flex;
    justify-content: center;
    align-items: center;
    width: inherit;
    gap: 10px;
    font-weight: 600;
    height: 60px;
    min-width: 160px;
    position: relative; // ✅ 必须！伪元素定位基准

    &::after {
        content: '';
        position: absolute;
        left: 50%;
        bottom: 6px;
        transform: translateX(-50%);
        width: 60px; // 下划线长度，自己调
        height: 2px; // 粗细
        background: linear-gradient(to right, #8bb9f6, #32589f 70%); // 线条颜色，用浅灰，不要太重
        border-radius: 4px;
    }

    .type-active {
        color: #20A090;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;

        .icon-active {
            cursor: pointer;

            &:hover {
                color: #3671C9;
            }
        }
    }
}
</style>