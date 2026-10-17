import * as echarts from 'echarts'
import type { EChartsOption, ECharts, ECElementEvent } from 'echarts'
import { shallowRef, onBeforeUnmount, onMounted, type Ref } from 'vue'

interface UseEChartsOptions {
    /** 静态基础配置（结构和样式，不含动态 data） */
    baseOption: EChartsOption
    /** 主题，可选 */
    theme?: string | object
}

export type EChartsClickHandler = (
    this: ECharts,
    params: ECElementEvent
) => boolean | void


export function useECharts(
    elRef: Ref<HTMLElement | undefined>,
    { baseOption, theme }: UseEChartsOptions,
    func?: EChartsClickHandler
) {
    // shallowRef 避免 Vue 深度代理 echarts 实例
    const chart = shallowRef<ECharts>()
    let resizeObserver: ResizeObserver | null = null

    const init = () => {
        if (!elRef.value) return
        chart.value = echarts.init(elRef.value, theme)
        // 基础配置只 setOption 一次
        chart.value.setOption(baseOption)
        if (func) {
            chart.value.on('click', func)
        }
    }

    /**
     * 更新数据
     * @param seriesData 单系列传 number[]，多系列传 number[][]
     */
    const updateData = (optionData: any, type: string) => {
        if (!chart.value) return

        if (type == 'map' || type == 'line') {
            chart.value.setOption({ ...optionData.chartOption })
        }

        if (type == 'bar') {
            let xAxis = optionData.map((tt: any) => tt.aiLabel)
            let data = optionData.map((tt: any) => tt.aiUseTotal)
            chart.value.setOption({ xAxis: { data: xAxis }, series: { id: 1, data } })
        }

        /*
        const isMulti = Array.isArray(seriesData[0])
        const series = isMulti
            ? (seriesData as number[][]).map((data) => ({ data }))
            : [{ data: seriesData as number[] }]

        chart.value.setOption({ series })
        */

    }

    /**
     * 整体替换 series（系列数量/名称会变化时用）
     */
    const replaceSeries = (series: EChartsOption['series']) => {
        chart.value?.setOption({ series }, { replaceMerge: 'series' })
    }

    /**
     * 更新任意部分配置（轴、标题等）
     */
    const updateOption = (partial: EChartsOption) => {
        chart.value?.setOption(partial)
    }

    const resize = () => chart.value?.resize()

    const showLoading = () => chart.value?.showLoading('default', { text: '加载中...' })
    const hideLoading = () => chart.value?.hideLoading()

    onMounted(() => {
        init()
        if (elRef.value) {
            resizeObserver = new ResizeObserver(resize)
            resizeObserver.observe(elRef.value)
        }
    })

    onBeforeUnmount(() => {
        resizeObserver?.disconnect()
        chart.value?.dispose()
        chart.value = undefined
    })

    return {
        chart,
        updateData,
        replaceSeries,
        updateOption,
        resize,
        showLoading,
        hideLoading,
    }
}