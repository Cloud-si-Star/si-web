<template>
    <div class="con-page">
        <div ref="chatRef" class="chatView"></div>
    </div>
</template>

<script setup lang="ts">
import { echartsKey } from '@/types/keys';
import type { ECharts, EChartsOption } from 'echarts';
import { inject,onBeforeUnmount,onMounted,ref, shallowRef } from 'vue';


const echarts =inject(echartsKey)!

const chatRef = ref<HTMLElement>()

const echartsInstance = shallowRef<ECharts>()

const option:EChartsOption={
    title:{
        text:'手写注册图表'
    },
    xAxis:{
        type:'category',
        data:['百度文心','通义千问','deepseek','chatGPT','KIMI']
    },
    yAxis:{
        type:'value'
    },
    tooltip:{
        show:true
    },
    series:[
        {
            type:'bar',
            data:[50,30,70,40,60],
            itemStyle:{
                color:{
                    type:'linear',
                    x:0.5,
                    y:0.5,
                    x2:0.7,
                    y2:0.9,
                    colorStops:[
                        {offset:0,color:'#4fc3ff'},
                        {offset:1,color:'#1a5fb4'}
                    ]
                }
            }
        }
    ]
}

const initchart = ()=>{
    if(!chatRef.value) return
    echartsInstance.value=echarts.init(chatRef.value,'')
    echartsInstance.value.setOption(option)
}

const resizeChart=()=>echartsInstance.value?.resize()

onMounted(()=>{
    initchart()
    window.addEventListener('resize',resizeChart)
})


onBeforeUnmount(()=>{
    window.removeEventListener('resize',resizeChart)
    echartsInstance.value?.dispose()
    echartsInstance.value=undefined
})

</script>

<style lang="scss" scoped>
.chatView{
    width: 100%;
    height: 100%;
}
</style>