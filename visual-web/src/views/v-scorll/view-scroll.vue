<template>
    <main class="screen-page">
        <header class="screen-header">
            <div class="brand-mark" aria-hidden="true">CN</div>
            <div class="header-copy">
                <p class="eyebrow">REGIONAL DATA OVERVIEW</p>
                <h1>全国数据运行总览</h1>
            </div>
            <div class="header-meta">
                <span class="live-dot"></span>
                <span>数据实时更新</span>
                <time>{{ currentTime }}</time>
            </div>
        </header>

        <section class="dashboard-grid">
            <SvgBorder class="map-panel" title="全国区域分布" title-position="top-left" color="#126b83" light-color="#57f3e5"
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
                        <vCommon :option="mapOption" />
                        <div class="map-caption">数据覆盖 <strong>34</strong> 个省级行政区</div>
                    </div>
                    <div class="metric-strip">
                        <div class="metric-item">
                            <span>今日访问量</span>
                            <strong>2,486,391</strong>
                            <small>较昨日 <b>+12.8%</b></small>
                        </div>
                        <div class="metric-item">
                            <span>活跃城市</span>
                            <strong>286</strong>
                            <small>覆盖率 <b>91.4%</b></small>
                        </div>
                        <div class="metric-item">
                            <span>平均响应</span>
                            <strong>126<em>ms</em></strong>
                            <small>服务状态 <b>稳定</b></small>
                        </div>
                    </div>
                </div>
            </SvgBorder>

            <div class="right-column">
                <SvgBorder class="chart-panel trend-panel" title="近七日访问趋势" title-position="top-left" color="#126b83"
                    light-color="#57f3e5" :stroke-width="1.2" :duration="5">
                    <div class="chart-content">
                        <div class="chart-summary">
                            <span>累计访问</span>
                            <strong>1,284,620</strong>
                            <b>+8.6%</b>
                        </div>
                        <vCommon :option="trendOption" />
                    </div>
                </SvgBorder>

                <SvgBorder class="chart-panel rank-panel" title="区域访问排行" title-position="top-left" color="#126b83"
                    light-color="#57f3e5" :stroke-width="1.2" :duration="5.8">
                    <div class="chart-content rank-content">
                        <div class="rank-note"><span>TOP 8</span><span>访问量 / 万</span></div>
                        <vCommon :option="rankOption" />
                    </div>
                </SvgBorder>
            </div>
        </section>
    </main>
</template>

<script setup lang="ts">
import { computed, inject, onBeforeUnmount, onMounted, ref } from 'vue'
import type { EChartsOption } from 'echarts'
import SvgBorder from '@/components/SvgBorder.vue'
import vCommon from '@/components/v-common.vue'
import chinaMap from '@/assets/maps/china.json'
import { echartsKey } from '@/types/keys'

interface RegionActivity {
    name: string
    value: number
}

const echarts = inject(echartsKey)

if (!echarts) {
    throw new Error('ECharts 尚未注入，请检查 main.ts 中的全局配置。')
}

// 注册本地省级 GeoJSON，保证地图不依赖运行时网络请求。
echarts.registerMap('china-regions', chinaMap as Parameters<typeof echarts.registerMap>[1])

const regions: RegionActivity[] = [
    { name: '广东', value: 96 },
    { name: '江苏', value: 88 },
    { name: '浙江', value: 83 },
    { name: '山东', value: 76 },
    { name: '四川', value: 69 },
    { name: '河南', value: 63 },
    { name: '湖北', value: 57 },
    { name: '福建', value: 52 },
    { name: '北京', value: 49 },
    { name: '上海', value: 46 },
    { name: '湖南', value: 43 },
    { name: '安徽', value: 39 },
    { name: '河北', value: 36 },
    { name: '辽宁', value: 32 },
    { name: '陕西', value: 29 },
    { name: '重庆', value: 27 },
    { name: '江西', value: 25 },
    { name: '云南', value: 22 },
    { name: '广西', value: 20 },
    { name: '黑龙江', value: 18 },
    { name: '吉林', value: 16 },
    { name: '山西', value: 15 },
    { name: '贵州', value: 14 },
    { name: '内蒙古', value: 13 },
    { name: '甘肃', value: 11 },
    { name: '新疆', value: 10 },
    { name: '海南', value: 9 },
    { name: '宁夏', value: 8 },
    { name: '青海', value: 7 },
    { name: '西藏', value: 5 },
    { name: '天津', value: 33 },
    { name: '香港', value: 24 },
    { name: '澳门', value: 12 },
    { name: '台湾', value: 31 },
]

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
    series: [{
        name: '区域活跃度',
        type: 'map',
        map: 'china-regions',
        roam: true,
        scaleLimit: { min: 0.8, max: 3 },
        zoom: 1.08,
        top: '5%',
        bottom: '8%',
        data: regions,
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
        label: { show: false },
    }],
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
        data: ['09/23', '09/24', '09/25', '09/26', '09/27', '09/28', '09/29'],
        axisLine: { lineStyle: { color: 'rgba(134, 180, 192, 0.28)' } },
        axisTick: { show: false },
        axisLabel: { color: '#819ca8', fontSize: 10 },
    },
    yAxis: {
        type: 'value',
        min: 0,
        max: 30,
        axisLabel: { color: '#819ca8', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(113, 161, 174, 0.13)', type: 'dashed' } },
    },
    series: [{
        name: '访问量',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        data: [16.2, 19.8, 18.4, 23.6, 21.9, 26.8, 28.4],
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
        data: regions.slice(0, 8).map((region) => region.name),
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#c4d5d9', fontSize: 11 },
    },
    series: [{
        name: '访问量',
        type: 'bar',
        barWidth: 10,
        data: regions.slice(0, 8).map((region, index) => ({
            value: region.value,
            itemStyle: {
                borderRadius: [0, 5, 5, 0],
                color: index < 3
                    ? { type: 'linear', x: 0, y: 0, x2: 1, y2: 0, colorStops: [{ offset: 0, color: '#168e91' }, { offset: 1, color: '#66f0dc' }] }
                    : { type: 'linear', x: 0, y: 0, x2: 1, y2: 0, colorStops: [{ offset: 0, color: '#24566a' }, { offset: 1, color: '#48aeb0' }] },
            },
        })),
        label: { show: true, position: 'right', color: '#b8d8d9', fontSize: 10 },
    }],
}

const now = ref(new Date())
const currentTime = computed(() => now.value.toLocaleString('zh-CN', { hour12: false }))
let clockTimer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
    clockTimer = setInterval(() => { now.value = new Date() }, 1000)
})

onBeforeUnmount(() => {
    if (clockTimer) clearInterval(clockTimer)
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
    justify-content: space-between;
    align-items: center;
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