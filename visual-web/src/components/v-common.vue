<template>
    <div ref="chartRef" class="common" :style="{width,height}"></div>
</template>

<script setup lang="ts">
import type { EChartsOption,ECharts,ECElementEvent } from 'echarts';
import { echartsKey } from '@/types/keys';   
import { inject,onBeforeUnmount,onMounted,ref, shallowRef, watch } from 'vue';


const props=withDefaults(defineProps<{
    option:EChartsOption
    width?:string
    height?:string
    theme?:string
}>(),{
    width:'100%',
    height:'100%',
    theme:undefined
})

const emit = defineEmits<{
    chartClick:[params:ECElementEvent]
}>()

// 注入echarts 
const echarts = inject(echartsKey)!
// 获取图表生成元素
const chartRef = ref<HTMLElement>()
// 定义图表实例
const echartsInstance = shallowRef<ECharts>()

// 初始化图表方法
const initChart=()=>{
    if(!chartRef.value) return 
    echartsInstance.value=echarts.init(chartRef.value,props.theme)
    echartsInstance.value?.setOption(props.option)
    echartsInstance.value.on('click',hanleChartClick)
}

// 定义一个窗口变化响应函数
const resizeChart = ()=>echartsInstance.value?.resize()

watch(
    // 监听option更新情况
    ()=>props.option,
    // 参数1表示新的option 参数2表示 不合并更新
    (newOption)=>echartsInstance.value?.setOption(newOption,true),
    // 深度检测
    {deep:true}
)


const hanleChartClick=(params:ECElementEvent)=>{
    emit('chartClick',params)
}

// 挂载完成后
onMounted(()=>{
    initChart()
    // 添加一个监听函数
    window.addEventListener('resize',resizeChart)
})

// 组件摧毁之前 消除图表
onBeforeUnmount(()=>{
    window.removeEventListener('resize',resizeChart)
    echartsInstance.value?.off('click',hanleChartClick)
    echartsInstance.value?.dispose()
    echartsInstance.value=undefined
})

defineExpose({
    resizeChart,
    getEchartsInstance:()=>echartsInstance.value
})

</script>

<style lang="scss" scoped>
.common{
    background: rgba(77, 95, 255, 0.12);
    border-radius: 8px;
}
</style>