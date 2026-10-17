<template>
  <div class="common-box">
    <div class="title-position">其实是用于标题 可以不写</div>
    <div class="common-ref" ref="chartRef"></div>
  </div>
</template>

<script setup lang="ts">
import { useECharts } from '@/views/v-scorll/useCharts'
import type { EChartsOption, ECElementEvent } from 'echarts';
import { ref, watch } from 'vue';

interface SettingItem {
  chartOption: any
  type: string
}

const props = withDefaults(defineProps<{
  baseOption: EChartsOption,
  baseSetting: SettingItem
  theme?: string
}>(), {})

const chartRef = ref<HTMLElement>()

const { baseOption, baseSetting } = props

const clickChartItem = (params: ECElementEvent) => {
  emit('chartClick', params)
}

const { updateData } = useECharts(chartRef, { baseOption }, clickChartItem)

watch(
  () => props.baseSetting,
  (newValue) => updateData(newValue, baseSetting.type),
  { deep: true }
)


const emit = defineEmits<{
  chartClick: [params: ECElementEvent]
}>()



</script>

<style lang="scss" scoped>
.common-box {
  height: 100%;
  width: 100%;
  position: relative;

  .title-position {
    position: absolute;
  }

  .common-ref {
    height: 100%;
    width: 100%;
    border: 1px solid #FFF;
  }
}
</style>