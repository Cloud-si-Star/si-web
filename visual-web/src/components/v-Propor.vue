<template>
    <div ref="chartRef" :style="{width,height}"></div>
</template>

<script setup lang="ts">
import { echartsKey } from '@/types/keys';
import type {ECharts, EChartsOption} from 'echarts'
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

const echarts = inject(echartsKey)!

const chartRef = ref<HTMLElement>()

const chartInstance = shallowRef<ECharts>()

watch(
    ()=>props.option,
    (newOption)=>chartInstance.value?.setOption(props.option,true),
    {deep:true}
)

const initChart = ()=>{
    if(!chartRef.value) return
    chartInstance.value = echarts.init(chartRef.value,props.theme)
    chartInstance.value?.setOption(props.option)
    console.log(props.option)
}
const resizeChart  = ()=>chartInstance.value?.resize()

onMounted(()=>{
    initChart()
    window.addEventListener('resize',resizeChart)
})

onBeforeUnmount(()=>{
    window.removeEventListener('resize',resizeChart)
    chartInstance.value?.dispose()
    chartInstance.value=undefined
})

defineExpose({
    initChart,
    getInstance:()=>chartInstance.value
})

</script>