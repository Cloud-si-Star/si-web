<template>
    <div class="app-all-box">
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
                <vPolar :option="polarOption"></vPolar>
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
                <vPropor :option="proporOption"></vPropor>
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
import type {EChartsOption} from "echarts"
import { ref,computed } from 'vue';
import { granda,funnel,pictor,propor,polar,gauge,parallel } from '@/utils/mock';

const vGrandpa_data=ref<EChartsOption>({
   visualMap:{
    min:0,
    max:10,
    inRange:{
        color: ['#4FD1C5', '#F6E05E', '#FC8181','#FC8181']
    }
   },
   series:{
    type:'sunburst',
    data:granda,
    radius:[0,'90%'],
    label:{
        rotate:'radial'
    }
   }

})

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
.app-all-box{
    height: 100%;
    box-sizing: border-box;
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f5a 45%, #412970 100%);
    display: flex;
    .third-box{
        flex: 1;
        height: 100%;
        border: 1px solid #FFF;
        display: flex;
        flex-direction: column;
        .echart-box{
            height: 100%;
            flex:1;
            border: 1px solid #CCC;
        }
    }
}
</style>