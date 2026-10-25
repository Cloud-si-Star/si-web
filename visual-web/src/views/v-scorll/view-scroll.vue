<template>
    <main class="screen-page">
        <!--
        <header class="screen-header">
            <div class="brand-mark" aria-hidden="true">CN</div>
            <div class="header-copy">
                <p class="eyebrow">REGIONAL DATA OVERVIEW</p>
                <h1>全国模型数据运行总览</h1>
            </div>
            <div class="header-meta">
                <span class="live-dot"></span>
                <span>数据实时更新</span>
                <time>{{ currentTime }}</time>
            </div>
        </header>
        -->

        <section class="dashboard-grid">
            <SvgBorder class="map-panel" title="" title-position="top-left" color="#126b83" light-color="#57f3e5"
                :stroke-width="1.4" :duration="4.5">
                <div class="map-content">
                    <div class="map-heading">
                        <div>
                            <span class="section-kicker">NATIONAL FOOTPRINT</span>
                            <h2>区域活跃度</h2>
                        </div>
                        <div class="map-legend"><i></i> 活跃指数</div>
                    </div>
                    <div class="map-stage">
                        <vConChart :base-option="mapOption" :base-setting="mapSetting" @chart-click="map_Query">
                        </vConChart>
                        <div class="map-caption">数据覆盖 <strong>34</strong> 个省级行政区</div>
                    </div>

                </div>
            </SvgBorder>

            <div class="right-column">
                <SvgBorder class="chart-panel trend-panel" :title="`${province_name}模型调用详情分布`"
                    title-position="top-right" color="#126b83" light-color="#57f3e5" :stroke-width="1.2" :duration="5">
                    <div class="chart-content">
                        <div class="chart-summary">
                            <span>累计访问</span>
                            <strong>1,284,620</strong>
                            <b>+8.6%</b>
                        </div>
                        <vPictorialBar :base-option="barBaseOption" :option-data="optionData"
                            @chartClick="query_by_ai_id" />
                    </div>
                </SvgBorder>

                <SvgBorder class="chart-panel rank-panel" :title="`${province_name}${ai_label}模型访问趋势`"
                    title-position="top-right" color="#126b83" light-color="#57f3e5" :stroke-width="1.2"
                    :duration="5.8">
                    <div class="chart-content rank-content">
                        <div class="rank-note"><span>TOP 8</span><span>访问量 / 万</span></div>
                        <vConChart :base-option="trendOption" :base-setting="lineSetting">
                        </vConChart>
                    </div>
                </SvgBorder>
            </div>
        </section>
    </main>
</template>

<script setup lang="ts">
import { computed, inject, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import type { EChartsOption, ECElementEvent } from 'echarts'
import SvgBorder from '@/components/SvgBorder.vue'
import vCommon from '@/components/v-common.vue'
import vPolar from '@/components/v-polar.vue'
import vPictorialBar from '@/components/v-PictorialBar.vue'

import vConChart from '@/components/v-con-chart.vue'

import chinaMap from '@/assets/maps/china.json'
import { echartsKey } from '@/types/keys'
import { chartsApi, formatNum, back_province_name, type DetailItem, type queryLine } from '@/api/charts'


/* =================右侧上方图表数据部分================= */
interface mapItem {
    name: string,
    value: number,
    adcode: number,
    selected?: boolean
}

const barBaseOption: EChartsOption = {
    backgroundColor: 'transparent',
    grid: { left: 48, right: 24, top: 8, bottom: 18 },
    tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(5, 20, 31, 0.94)',
        borderColor: 'rgba(87, 243, 229, 0.4)',
        textStyle: { color: '#e7fbff' },
    },
    xAxis: {
        type: 'category',
        axisLabel: {
            color: '#819ca8',
            fontSize: 10,
            formatter: function (value) {
                if (!value.trim()) return value
                let result = value.split(' ')[0]!
                return result;
            }
        },
        data: [],
    },
    yAxis: {
        type: 'value',
        splitLine: { lineStyle: { color: 'rgba(113, 161, 174, 0.13)', type: 'dashed' } },
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#c4d5d9', fontSize: 11 },
    },
    series: [
        {
            id: 1,
            name: '模型使用量',
            type: 'bar',
            barWidth: 10,
            data: [],
            itemStyle: {
                borderRadius: [5, 5, 0, 0],
                color: { type: 'linear', x: 1, y: 1, x2: 0, y2: 0, colorStops: [{ offset: 0, color: '#168e91' }, { offset: 1, color: '#66f0dc' }] }
            },
            label: {
                show: true,
                position: 'top',
                color: '#b8d8d9',
                fontSize: 10,
                formatter: function (params) {
                    return formatNum(Number(params.value))
                }
            },
        },
    ],
}

const optionData = ref<DetailItem[]>([])

const province_name = ref<string | undefined>('')

const ai_label = ref<string | undefined>('')

const query_ai_detail_by_province_id = async (adcode: number | undefined) => {
    try {
        optionData.value = await chartsApi.getDetailByProvinceId(adcode)

        province_name.value = back_province_name(adcode)

        if (optionData.value.length > 0) {
            let tt = optionData.value[0]
            ai_label.value = tt?.aiLabel
            queryline({ provinceId: adcode!, aiId: tt?.aiId! })
        }

    } catch (error) {
        console.log(error);
    }
}


const scatterData = ref<mapItem[]>([])

/* 挂载后获取省份数据 */
const query_province_total = async () => {
    try {
        const response = await chartsApi.getProvinceTotalDistrition()
        scatterData.value = response.map((tt) => {

            let ttItem: mapItem = {
                name: tt.aiUseProvince,
                value: tt.aiUseTotal,
                adcode: tt.aiUseProvinceId
            }

            if (tt.aiUseProvinceId == 110000) {
                ttItem = { ...ttItem, selected: true }
            }

            return ttItem
        })

        let rangArray = scatterData.value.map(tt => tt.value)

        let [min, max] = rangArray.reduce(
            ([mn, mx], v) => [v < mn ? v : mn, v > mx ? v : mx],
            [Infinity, -Infinity]
        )

        let option = {
            visualMap: {
                min: min,
                max: max
            },
            series: [
                {
                    id: 1,
                    data: scatterData.value
                }
            ]
        }

        mapSetting.value.chartOption = option

    } catch (error) {
        console.log(error);
    }
}

const adcode = ref(0)

const map_Query = (params: ECElementEvent) => {
    if (!params) return
    try {
        const { data, name } = params

        query_ai_detail_by_province_id(data!.adcode)
        adcode.value = data?.adcode!

    } catch (err) {
        console.log(err);
    }
}

const query_by_ai_id = (params: ECElementEvent) => {
    if (!params) return
    try {
        const { data, name } = params
        ai_label.value = name
        queryline({ provinceId: adcode.value, aiId: data?.aiId! })

    } catch (error) {

    }
}

/* =================左侧地图图表数据部分================= */
const mapOption: EChartsOption = {
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
    visualMap: {
        show: false,
        min: 0,
        max: 100,
        inRange: { color: ['#102b3a', '#145467', '#168b91', '#66e6d3'] },
    },
    geo: {
        map: 'china-regions',
        roam: true,
        label: {
            show: false,
        },
        scaleLimit: { min: 0.8, max: 3 },
        zoom: 1.08,
        select: {
            itemStyle: {
                areaColor: '#e05a4f',      // 见下方推荐色
                borderColor: '#ffffff',
                borderWidth: 1.5
            },
            label: { show: true, color: '#fff' }
        },
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
        }
    },
    series: [
        {
            name: '调用量',
            type: 'map',
            id: 1,
            map: 'china-regions',
            selectedMode: 'single',
            geoIndex: 0, // ★ 关键：复用上面那个 geo，不重画底图
            roam: true,
            data: scatterData.value,
        },
        {
            type: 'scatter',
            id: 2,
            coordinateSystem: 'geo',
            geoIndex: 0,
            encode: {
                // `2` is the dimension index of series.data
                tooltip: 2,
                label: 2
            },
            data: [],
            itemStyle: {
                color: '#66c2a5',
                borderWidth: 1,
                borderColor: '#3c7865'
            }
        },
    ]
}

const echarts = inject(echartsKey)

if (!echarts) {
    throw new Error('ECharts 尚未注入，请检查 main.ts 中的全局配置。')
}

// 注册本地省级 GeoJSON，保证地图不依赖运行时网络请求。
echarts.registerMap('china-regions', chinaMap as Parameters<typeof echarts.registerMap>[1])

const mapSetting = ref({
    chartOption: {},
    type: 'map'
})

const lineSetting = ref({
    chartOption: {},
    type: 'line'
})

const queryline = async (params: queryLine) => {
    try {
        const response = await chartsApi.getDetailByProAndAiIDs(params)
        let option = {
            xAxis: {
                data: response.map(tt => tt.month)
            },
            series: [
                {
                    id: 1,
                    data: response.map(tt => tt.value)
                }
            ]
        }
        lineSetting.value.chartOption = option
    } catch (error) {
        console.log(error);
    }
}




const trendOption: EChartsOption = {
    backgroundColor: 'transparent',
    grid: { left: 42, right: 16, top: 24, bottom: 26 },
    tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(5, 20, 31, 0.94)',
        borderColor: 'rgba(87, 243, 229, 0.4)',
        textStyle: { color: '#e7fbff' },
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: [],
        axisLine: { lineStyle: { color: 'rgba(134, 180, 192, 0.28)' } },
        axisTick: { show: false },
        axisLabel: { color: '#819ca8', fontSize: 10 },
    },
    yAxis: {
        type: 'value',
        axisLabel: { color: '#819ca8', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(113, 161, 174, 0.13)', type: 'dashed' } },
    },
    series: [{
        name: '访问量',
        type: 'line',
        id: 1,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        data: [],
        lineStyle: { color: '#56eee0', width: 2 },
        itemStyle: { color: '#a8fff4', borderColor: '#1a938d', borderWidth: 2 },
        areaStyle: {
            color: {
                type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                    { offset: 0, color: 'rgba(48, 222, 207, 0.28)' },
                    { offset: 1, color: 'rgba(48, 222, 207, 0.01)' },
                ],
            },
        },
    }],
}

const rankOption: EChartsOption = {
    backgroundColor: 'transparent',
    grid: { left: 48, right: 24, top: 8, bottom: 18 },
    tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(5, 20, 31, 0.94)',
        borderColor: 'rgba(87, 243, 229, 0.4)',
        textStyle: { color: '#e7fbff' },
    },
    xAxis: {
        type: 'value',
        axisLabel: { color: '#819ca8', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(113, 161, 174, 0.13)', type: 'dashed' } },
    },
    yAxis: {
        type: 'category',
        inverse: true,
        // data: regions.slice(0, 8).map((region) => region.name),
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#c4d5d9', fontSize: 11 },
    },
    series: [{
        name: '访问量',
        type: 'bar',
        barWidth: 10,
        // data: regions.slice(0, 8).map((region, index) => ({
        //     value: region.value,
        //     itemStyle: {
        //         borderRadius: [0, 5, 5, 0],
        //         color: index < 3
        //             ? { type: 'linear', x: 0, y: 0, x2: 1, y2: 0, colorStops: [{ offset: 0, color: '#168e91' }, { offset: 1, color: '#66f0dc' }] }
        //             : { type: 'linear', x: 0, y: 0, x2: 1, y2: 0, colorStops: [{ offset: 0, color: '#24566a' }, { offset: 1, color: '#48aeb0' }] },
        //     },
        // })),
        label: { show: true, position: 'right', color: '#b8d8d9', fontSize: 10 },
    }],
}

onMounted(() => {
    query_province_total()
    // 110000这是北京 默认北京数据
    query_ai_detail_by_province_id(110000)
})

</script>

<style scoped lang="scss">
.screen-page {
    --screen-bg: #061116;
    --screen-text: #e5f5f5;
    --screen-muted: #7e9ba3;
    width: 100%;
    height: 100%;
    min-height: 620px;
    overflow: hidden;
    padding: 22px 24px 24px;
    color: var(--screen-text);
    background:
        radial-gradient(ellipse at 31% 45%, rgba(12, 80, 86, 0.17), transparent 42%),
        linear-gradient(135deg, #07151b 0%, #081116 54%, #101a1d 100%);
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.screen-header {
    flex: 0 0 66px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 1px solid rgba(87, 243, 229, 0.15);
}

.brand-mark {
    width: 42px;
    height: 42px;
    display: grid;
    place-items: center;
    border: 1px solid rgba(87, 243, 229, 0.58);
    color: #80fff0;
    font-size: 13px;
    font-weight: 700;
    text-shadow: 0 0 12px rgba(87, 243, 229, 0.5);
}

.header-copy h1 {
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0;
}

.eyebrow,
.section-kicker {
    color: #61c7c3;
    font-size: 9px;
    line-height: 1.4;
    letter-spacing: 1.3px;
}

.header-meta {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 9px;
    color: #92abb1;
    font-size: 12px;
}

.header-meta time {
    margin-left: 14px;
    color: #d0e3e5;
    font-variant-numeric: tabular-nums;
}

.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #54ecd4;
    box-shadow: 0 0 10px #54ecd4;
}

.dashboard-grid {
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(330px, 1fr);
    gap: 18px;
}

.map-panel,
.right-column,
.chart-panel {
    min-width: 0;
    min-height: 0;
}

.map-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 15px 18px 13px;
}

.map-heading {
    flex: 0 0 52px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    position: absolute;
}

.map-heading h2 {
    margin-top: 2px;
    font-size: 17px;
    font-weight: 500;
}

.map-legend {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #8da7ac;
    font-size: 11px;
    margin-top: 5px;
}

.map-legend i {
    width: 24px;
    height: 5px;
    background: linear-gradient(90deg, #123c4b, #66e6d3);
}

.map-stage {
    flex: 1;
    position: relative;
    min-height: 0;
}

.map-stage :deep(.common) {
    background: transparent;
}

.map-caption {
    position: absolute;
    right: 10px;
    bottom: 8px;
    color: #7e9ba3;
    font-size: 11px;
    pointer-events: none;
}

.map-caption strong {
    padding: 0 3px;
    color: #73eee0;
    font-size: 15px;
}

.metric-strip {
    flex: 0 0 96px;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    border-top: 1px solid rgba(100, 183, 188, 0.19);
}

.metric-item {
    padding: 12px 12px 0;
    display: flex;
    flex-direction: column;
    gap: 3px;
    border-right: 1px solid rgba(100, 183, 188, 0.12);
}

.metric-item:last-child {
    border-right: 0;
}

.metric-item>span,
.metric-item small {
    color: #79969d;
    font-size: 10px;
}

.metric-item strong {
    color: #e1ffff;
    font-size: 21px;
    line-height: 1.2;
    font-variant-numeric: tabular-nums;
}

.metric-item em {
    margin-left: 3px;
    color: #7dabb0;
    font-size: 11px;
    font-style: normal;
}

.metric-item small b {
    margin-left: 3px;
    color: #63e3c9;
    font-weight: 500;
}

.right-column {
    display: grid;
    grid-template-rows: minmax(0, 1fr) minmax(0, 1fr);
    gap: 18px;
}

.chart-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 14px 14px 12px;
}

.chart-summary {
    flex: 0 0 44px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: #87a2a9;
    font-size: 11px;
}

.chart-summary strong {
    color: #e2ffff;
    font-size: 18px;
    font-variant-numeric: tabular-nums;
}

.chart-summary b {
    color: #64e5c9;
    font-size: 10px;
    font-weight: 500;
}

.chart-content :deep(.common) {
    flex: 1;
    min-height: 0;
    background: transparent;
}

.rank-note {
    flex: 0 0 23px;
    display: flex;
    justify-content: space-between;
    color: #77959d;
    font-size: 10px;
}

.rank-note span:first-child {
    color: #65dcd3;
    letter-spacing: 1px;
}

@media (max-width: 900px) {
    .screen-page {
        height: auto;
        min-height: 100%;
        overflow: auto;
        padding: 16px;
    }

    .dashboard-grid {
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: minmax(480px, 58vh) minmax(600px, 1fr);
    }

    .right-column {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        grid-template-rows: minmax(330px, 1fr);
    }
}

@media (max-width: 600px) {
    .screen-page {
        gap: 14px;
        padding: 12px;
    }

    .screen-header {
        flex-basis: 58px;
        gap: 10px;
    }

    .brand-mark {
        width: 36px;
        height: 36px;
    }

    .header-copy h1 {
        font-size: 17px;
    }

    .eyebrow {
        font-size: 8px;
    }

    .header-meta {
        align-items: flex-end;
        flex-direction: column;
        gap: 2px;
        font-size: 9px;
    }

    .header-meta time {
        margin-left: 0;
        font-size: 9px;
    }

    .dashboard-grid {
        grid-template-rows: minmax(420px, 62vh) minmax(650px, auto);
        gap: 14px;
    }

    .right-column {
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: repeat(2, minmax(300px, 1fr));
        gap: 14px;
    }

    .map-content {
        padding: 13px 10px 10px;
    }

    .metric-strip {
        flex-basis: 84px;
    }

    .metric-item {
        padding: 10px 6px 0;
    }

    .metric-item strong {
        font-size: 16px;
    }

    .metric-item>span,
    .metric-item small {
        font-size: 9px;
    }
}
</style>