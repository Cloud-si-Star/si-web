<template>
    <div ref="chartRef" class="common" :style="{width,height}">

    </div>
</template>

<script setup lang="ts">
import {watch,ref,onMounted,onBeforeUnmount,shallowRef,inject} from 'vue'
import { echartsKey } from '@/types/keys';
import type { EChartsOption,ECharts } from 'echarts';

const props =withDefaults(defineProps<{
    option:EChartsOption
    width?:string,
    height?:string,
    theme?:string
}>(),{
    width:'100%',
    height:'100%',
    theme:'westeros'
})


const echarts = inject(echartsKey)!

const chartRef=ref<HTMLElement>()!

const chartInstance = shallowRef<ECharts>()

const currentSpeed =ref<Number>(70)

let timer: ReturnType<typeof setInterval> | null = null


const initChart=()=>{
    
    if(!chartRef.value) return
    chartInstance.value = echarts.init(chartRef.value, props.theme)
    chartInstance.value.setOption(props.option)
}

const resizeChart = ()=>chartInstance.value?.resize()

watch(
    ()=>props.option,
    (newOption)=>chartInstance.value?.setOption(newOption,true),
    {deep:true}
)


// 定时修改数值
function startAnimate() {
   timer = setInterval(() => {
    // 模拟波动，随机在 40~80之间变化
    currentSpeed.value = Math.floor(Math.random() * 40) + 40
    // ✅ 更新series的数据
    if(!props.option.series) return
    props.option.series[0].data=[
        {
            value: currentSpeed.value,
            detail: {
                fontSize: 16
            }
        }
    ]

  }, 6000)
}

function stopAnimate() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}


onMounted(()=>{
    initChart()
    startAnimate()
    window.addEventListener('resize',resizeChart)
})

onBeforeUnmount(()=>{
    stopAnimate()
    window.removeEventListener('resize',resizeChart)
    chartInstance.value?.dispose()
    chartInstance.value=undefined
})

defineExpose({
    resizeChart,
    getInstance:()=>chartInstance.value
})

</script>

<style lang="scss" scoped>
.common{
    background: rgba(77, 95, 255, 0.12);
    border-radius: 8px;
}
</style>