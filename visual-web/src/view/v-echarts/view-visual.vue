<template>
    
    <div class="app-all-box ">
      
       <div class="third-box">
            <div class="echart-box">
                <vCommon :option="vLine_dataOpt"></vCommon>
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
import type {EChartsOption} from "echarts"
import { ref,computed } from 'vue';
import { grdopt,funnel,pictor,propor,polar,gauge,parallel } from '@/utils/mock';
// 引入模拟数据 静态数据
import {worldPopulationLine,countryPopBar,continentPie,urbanRing} from '@/utils/mock_v1'

import {vLine_dataOpt,vBar_dataOpt,middleoption,middle_3_option,middle_2_option} from './v-api.ts'

/* -----------------左上折线图----------------- */
// 数据是对象数组 要把数据拆分 赋值给折线图



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