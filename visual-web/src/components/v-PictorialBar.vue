<template>
    <div class="common">
        <div ref="chartRef" class="chart" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import type { EChartsOption, ECElementEvent } from 'echarts'
import { useECharts } from '@/views/v-scorll/useCharts'


const props = withDefaults(defineProps<{
    baseOption: EChartsOption
    optionData: any
}>(), {

})

const chartRef = ref<HTMLElement>()

/**
const baseOption: EChartsOption = {
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 40, bottom: 40 },
    xAxis: {
        type: 'category',
        data: ['一月', '二月', '三月', '四月', '五月', '六月'],
    },
    yAxis: { type: 'value', name: '万元' },
    series: [
        {
            name: '销售额',
            type: 'line',
            smooth: true,
            areaStyle: { opacity: 0.15 },
            data: [],
        },
    ],
}

 */
const { baseOption, optionData } = props

const emit = defineEmits<{
    chartClick: [params: ECElementEvent]
}>()

const clickChartItem = (params: ECElementEvent) => {
    emit('chartClick', params)
}

const { updateData, showLoading, hideLoading } = useECharts(chartRef, { baseOption }, clickChartItem)


watch(
    () => props.optionData,
    (newValue) => updateData(newValue, 'bar')
)

</script>



<style scoped>
.common {
    position: relative;
}

.chart {
    width: 100%;
    height: 100%;
}
</style>