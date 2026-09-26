<template>
    
    <div class="app-all-box ">
      
       <div class="third-box">
            <div class="echart-box">
                <vCommon :option="vLine_dataOpt" @chartClick="hanleParams"></vCommon>
            </div>
            <div class="echart-box">
                <vCommon :option="vBar_dataOpt"></vCommon>
            </div>
       </div>
       <div class="third-box unique-common">
            <div class="echart-box">
                
                <!-- 这里放 echarts 容器 -->
                <vFunnel :option="middleoption"></vFunnel>
                
            </div>

            <div class="echart-box">
                <vCommon :option="middle_2_option"></vCommon>
            </div>
           
            <div class="echart-box">
                <vCommon :option="middle_3_option"></vCommon>
            </div>

       </div>
       <div class="third-box">
            <div class="echart-box">
                <vCommon :option="parallelOption"></vCommon>
            </div>
            <div class="echart-box">
                <vPropor></vPropor>
            </div>
       </div>
      
    </div>
   
</template>

<script lang="ts" setup>
import vCommon from '@/components/v-common.vue';
import vPropor from '@/components/v-Propor.vue';
import vFunnel from '@/components/v-Funnel.vue';
import type {EChartsOption,ECElementEvent} from "echarts"
import * as echarts from 'echarts'
import { ref,computed, onBeforeUnmount, watch,onBeforeMount } from 'vue';
import { grdopt,funnel,pictor,propor,polar,gauge,parallel } from '@/utils/mock';
// 引入模拟数据 静态数据
import {worldPopulationLine,countryPopBar,continentPie,urbanRing} from '@/utils/mock_v1'

import {vLine_dataOpt,middleoption,middle_3_option,middle_2_option} from './v-api.ts'
import {useAiStore} from '@/stores/ai_item.ts'
import { storeToRefs } from 'pinia';


/* 对于柱状图数据的修改 */
const useAi = useAiStore()

const {aiTable} = storeToRefs(useAi)

let vBar_dataOpt=ref<EChartsOption |null>(null)

const chart_bar_data = computed(() => {
    const x: string[] = []
    const y: number[] = []
    aiTable.value.forEach(i => {
        x.push(i.ai_name)
        y.push(i.ai_use)
    })
    console.log(123);

    return { x, y }
})


const initBar=()=>{
  vBar_dataOpt={
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        },
        backgroundColor: 'rgba(112, 98, 235,0.15)',
        textStyle: {
            color: '#FFF'
        }
    },
    xAxis: {
        type: 'category',
        data: chart_bar_data.value.x,
        axisTick: {
            alignWithLabel: true
        },
        axisLabel: {
            color: '#e8e8e8',
            rotate: 45,
            margin: 12
        },
    },

    yAxis: {
        type: 'value',
        axisLabel: {
            color: '#e8e8e8',
        },
        splitLine: {
            show: true, // 纵向网格线（x轴分割线）
            lineStyle: {
                type: 'dashed', // 虚线
                color: 'rgba(120,150,180,0.25)', // 浅色，调低透明度
                width: 1
            }
        }
    },
    series: [
        {
            name: 'Direct',
            type: 'bar',
            barWidth: '60%',
            data: chart_bar_data.value.y,
            itemStyle: {
                color: new echarts.graphic.LinearGradient(
                    0, 0, 0, 1,
                    [
                        { offset: 0, color: '#edafda' },
                        { offset: 1, color: '#a5e7f0' }
                    ]
                )
            }
        }
    ]
  }
}

  
onBeforeMount(()=>{
  initBar()
})

watch(aiTable,initBar,{deep:true})

/* -----------------左上折线图----------------- */
// 数据是对象数组 要把数据拆分 赋值给折线图
const hanleParams=(params:ECElementEvent)=>{
  console.log(params);
  
}


/* -----------------左下柱状图----------------- */
// 数据是对象数组 要把数据拆分 赋值给折线图


// 中间1 饼图
const vPieopt = {
  title: {
    text: 'Referer of a Website',
    subtext: 'Fake Data',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      data: continentPie,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};




// 环形图
const vHuanOpt = {
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: urbanRing
    }
  ]
};

const pictorOption = ref<EChartsOption>(pictor)


const gaugeOption = ref<EChartsOption>(gauge)

const parallelOption = ref<EChartsOption>(parallel)


</script>

<style lang="scss" scoped>
// 变量：青蓝色系 + 边框参数


.app-all-box{
    height: 100%;
    box-sizing: border-box;
    background:
        // 光晕
        radial-gradient(ellipse 80% 50% at 50% 0%, rgba(0, 229, 255, 0.45), transparent 70%),
        linear-gradient(160deg, #0a1628 0%, #061020 50%, #3e5c98 100%);
   
    display: flex;
    padding: 5px;
    .third-box{
        flex: 1;
        height: 100%;
        display: flex;
        flex-direction: column;
        .echart-box{
            height: 100%;
            flex:1;
            margin:5px ;
            padding: 5px;
            
            overflow: hidden;
        }
    }
    .unique-common{
      flex: 0.7;
    }
}

</style>