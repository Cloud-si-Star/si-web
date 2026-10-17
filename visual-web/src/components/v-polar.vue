<template>
  <div ref="chartRef" class="common" :style="{ width, height }"></div>
</template>

<script setup lang="ts">
import type { EChartsOption, ECharts, ECElementEvent } from 'echarts';
import { echartsKey } from '@/types/keys';
import { inject, onBeforeUnmount, onMounted, ref, shallowRef, watch, computed } from 'vue';

interface mapItem {
  name: string,
  value: number
}

const props = withDefaults(defineProps<{
  mapItemData: mapItem[]
  width?: string
  height?: string
  theme?: string
}>(), {
  width: '100%',
  height: '100%',
  theme: undefined
})

const emit = defineEmits<{
  chartClick: [params: ECElementEvent]
}>()

// 注入echarts 
const echarts = inject(echartsKey)!
// 获取图表生成元素
const chartRef = ref<HTMLElement>()
// 定义图表实例
const echartsInstance = shallowRef<ECharts>()

const mapOption = ref<EChartsOption>({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(5, 20, 31, 0.94)',
    borderColor: 'rgba(87, 243, 229, 0.55)',
    textStyle: { color: '#e7fbff' },
    formatter: (params) => {
      const item = Array.isArray(params) ? params[0] : params
      return `${item?.name ?? '区域'}<br/>活跃指数：${item?.value ?? '暂无数据'}`
    },
  },

  geo: {
    map: 'china-regions',
    roam: true,
    label: {
      show: false,
    },
    scaleLimit: { min: 0.8, max: 3 },
    zoom: 1.25,
    // left: 20,
    // top: 20,
    // right: 20,
    // bottom: 20,

    itemStyle: {
      borderColor: 'rgba(135, 240, 234, 0.64)',
      borderWidth: 0.8,
      areaColor: '#102b3a',
      shadowColor: 'rgba(31, 222, 211, 0.28)',
      shadowBlur: 8,
    },
    emphasis: {
      label: { show: true, color: '#f2ffff', fontSize: 11 },
      itemStyle: { areaColor: '#36b9ad', borderColor: '#b5fff4', borderWidth: 1.2 },
    },
  }
})

function updateData() {
  let rangArray = props.mapItemData.map(tt => tt.value)

  let [min, max] = rangArray.reduce(
    ([mn, mx], v) => [v < mn ? v : mn, v > mx ? v : mx],
    [Infinity, -Infinity]
  )



  mapOption.value = {
    ...mapOption.value,
    visualMap: {
      show: false,
      min: min,
      max: max,
      inRange: {
        color: [
          '#0b2545',  // 深海军蓝
          '#13315c',  // 蓝
          '#1a5b8a',  // 中蓝
          '#1e88a8',  // 青蓝
          '#26b5a8',  // 青绿
          '#4ee0b0',  // 亮绿
          '#a6ffcb',  // 极亮
        ]
      }
    },
    series: [
      {
        name: '区域活跃度',
        type: 'map',
        map: 'china-regions',
        geoIndex: 0, // ★ 关键：复用上面那个 geo，不重画底图
        roam: true,
        data: props.mapItemData,
      },
      {
        type: 'scatter',
        coordinateSystem: 'geo',
        geoIndex: 0,
        encode: {
          // `2` is the dimension index of series.data
          tooltip: 2,
          label: 2
        },
        data: [
          [127.693027, 48.040465, 14523],
          [127.693027, 48.040465, 14523],
          [106.278179, 38.46637, 14523],

        ],
        itemStyle: {
          color: '#66c2a5',
          borderWidth: 1,
          borderColor: '#3c7865'
        }
      },
    ],
  }

  initChart()
}

// 初始化图表方法
const initChart = () => {
  if (!chartRef.value) return
  echartsInstance.value = echarts.init(chartRef.value, props.theme)
  echartsInstance.value?.setOption(mapOption.value)
  echartsInstance.value.on('click', hanleChartClick)
}

// 定义一个窗口变化响应函数
const resizeChart = () => echartsInstance.value?.resize()

watch(
  // 监听option更新情况
  () => props.mapItemData,
  // 参数1表示新的option 参数2表示 不合并更新
  (newOption) => updateData(),
  // 深度检测
  { deep: true }
)


const hanleChartClick = (params: ECElementEvent) => {

  emit('chartClick', params)
}

// 挂载完成后
onMounted(() => {
  initChart()
  // 添加一个监听函数
  window.addEventListener('resize', resizeChart)
})

// 组件摧毁之前 消除图表
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  echartsInstance.value?.off('click', hanleChartClick)
  echartsInstance.value?.dispose()
  echartsInstance.value = undefined
})

defineExpose({
  resizeChart,
  initChart,
  getEchartsInstance: () => echartsInstance.value
})

</script>

<style lang="scss" scoped>
.common {
  background: rgba(77, 95, 255, 0.12);
  border-radius: 8px;
}
</style>