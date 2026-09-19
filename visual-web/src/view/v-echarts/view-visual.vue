<template>
    <div class="app-all-box ">
       <div class="third-box">
            <div class="echart-box">
                <vGrandpa :option="vGrandpaOption"></vGrandpa>
            </div>
            <div class="echart-box">
                <vFunnel :option="vFunnelOpt"></vFunnel>
            </div>
       </div>
       <div class="third-box">
            <div class="echart-box">
                <SvgBorder
                    title="实时流量监控"
                    title-position="top-left"
                    color="#0891b2"
                    light-color="#00e5ff"
                    :stroke-width="1.5"
                    :radius="10"
                    :duration="3"
                    >
                    <!-- 这里放 echarts 容器 -->
                    <vFunnel :option="polarOption"></vFunnel>
                </SvgBorder>
            </div>
            <div class="echart-box">
                <vPolar :option="gaugeOption"></vPolar>
            </div>
            <div class="echart-box">
                <vPolar :option="parallelOption"></vPolar>
            </div>
       </div>
       <div class="third-box">
            <div class="echart-box">
                <vPictorialBar :option="vPictortion"></vPictorialBar>
            </div>
            <div class="echart-box">
                <vPictorialBar :option="proporOption"></vPictorialBar>
            </div>
       </div>
       
    </div>
</template>

<script lang="ts" setup>
import vGrandpa from '@/components/v-Grandpa.vue';
import vFunnel from '@/components/v-Funnel.vue';
import vPictorialBar from '@/components/v-PictorialBar.vue';
import vPropor from '@/components/v-Propor.vue';
import vPolar from '@/components/v-polar.vue';
import SvgBorder from '@/components/SvgBorder.vue'
import type {EChartsOption} from "echarts"
import { ref,computed } from 'vue';
import { grdopt,funnel,pictor,propor,polar,gauge,parallel } from '@/utils/mock';

const vGrandpa_data=ref<EChartsOption>(grdopt)

const vGrandpaOption=computed(()=>{
    return vGrandpa_data.value
})


const vFunnelOption=ref<EChartsOption>(funnel)

const vFunnelOpt=computed(()=>{
    return vFunnelOption.value
})


const vPictortion = ref<EChartsOption>(pictor)

const proporOpt = ref<EChartsOption>(propor)

const proporOption = computed(()=>proporOpt.value)

const polarOption = ref<EChartsOption>(polar)

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
}

</style>