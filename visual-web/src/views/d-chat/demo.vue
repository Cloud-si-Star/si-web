<template>
    <div class="con-page">
        <vVirtual :list="arr"></vVirtual>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import vVirtual from '@/components/v-virtual.vue';

const arr = Array.from({ length: 20 }, (_, i: number) => ({
    id: i + 1,
    name: `这是一条长文字数据，这是第${i}条，共10条`
}))


onMounted(() => {
    console.log(arr);
})
</script>

<style lang="scss" scoped>
.virtual-box {
    box-sizing: border-box;
    height: 200px;
    width: 400px;
    background-color: rgba(127, 255, 212, 0.3);
    overflow: auto;
}
</style>