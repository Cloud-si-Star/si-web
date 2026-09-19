<template>
  <div ref="chartRef" :style="{ width, height }"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, shallowRef, inject } from 'vue'
import { echartsKey } from '@/types/keys'
import type { EChartsOption, ECharts } from 'echarts'

const props = withDefaults(defineProps<{
  option: EChartsOption
  width?: string
  height?: string
  theme?: string | object
}>(), {
  width: '100%',
  height: '100%',
  theme: undefined,
})

// 注入 echarts，类型自动推断为 typeof import('echarts')
const echarts = inject(echartsKey)!

const chartRef = ref<HTMLElement>()
const chartInstance = shallowRef<ECharts>()

const initChart = () => {
  if (!chartRef.value) return
  chartInstance.value = echarts.init(chartRef.value, props.theme)
  chartInstance.value.setOption(props.option)
}

const resizeChart = () => chartInstance.value?.resize()

watch(
  () => props.option,
  (newOption) => chartInstance.value?.setOption(newOption, true),
  { deep: true }
)

onMounted(() => {
  initChart()
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chartInstance.value?.dispose()
  chartInstance.value = undefined
})

defineExpose({ resizeChart, getInstance: () => chartInstance.value })
</script>