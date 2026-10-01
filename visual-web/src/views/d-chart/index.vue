<template>
    <main class="chart-editor">
        <header class="editor-header">
            <div class="heading-copy">
                <span class="eyebrow">VISUAL WORKBENCH / CHART STUDIO</span>
                <h1>图表编辑器</h1>
            </div>
            <div class="header-actions">
                <span class="save-state"><i></i> 本地实时预览</span>
                <el-button :icon="RefreshLeft" @click="resetConfig">重置配置</el-button>
                <el-button type="primary" :icon="Download" @click="downloadConfig">导出配置</el-button>
            </div>
        </header>

        <section class="studio-layout">
            <aside class="type-rail" aria-label="图表类型">
                <div class="rail-heading">
                    <span class="step-number">01</span>
                    <div>
                        <h2>图表类型</h2>
                        <p>选择一种呈现方式</p>
                    </div>
                </div>
                <div class="chart-type-list">
                    <button v-for="chart in chartTypes" :key="chart.value" type="button" class="chart-type-option"
                        :class="{ selected: chartType === chart.value }" :aria-pressed="chartType === chart.value"
                        @click="chartType = chart.value">
                        <el-icon>
                            <component :is="chart.icon" />
                        </el-icon>
                        <span>{{ chart.label }}</span>
                        <span class="type-mark">{{ chart.mark }}</span>
                    </button>
                </div>
                <div class="rail-footnote"><span>5</span> 种图表</div>
            </aside>

            <section class="preview-area" aria-label="图表预览">
                <div class="preview-toolbar">
                    <div>
                        <span class="step-number">02</span>
                        <div>
                            <h2>实时预览</h2>
                            <p>{{ activeChartLabel }} · {{ datasetLabel }}</p>
                        </div>
                    </div>
                    <el-tag effect="plain" type="success">LIVE</el-tag>
                </div>

                <div class="preview-frame" :class="`theme-${theme}`">
                    <div class="preview-chart-heading">
                        <span>{{ chartTitle || '未命名图表' }}</span>
                        <small>{{ dataset.length }} 个数据项</small>
                    </div>
                    <div class="chart-canvas">
                        <vCommon :option="chartOption" />
                    </div>
                    <div class="preview-footer">
                        <span><i :style="{ backgroundColor: seriesColor }"></i>{{ seriesLabel }}</span>
                        <span>{{ chartType === 'pie' || chartType === 'donut' ? '占比视图' : '趋势视图' }}</span>
                    </div>
                </div>

                <div class="preview-caption">
                    <span>当前数据源</span>
                    <strong>{{ datasetLabel }}</strong>
                    <span class="caption-divider"></span>
                    <span>{{ formatNumber(datasetTotal) }} 合计</span>
                </div>
            </section>

            <aside class="config-panel" aria-label="图表配置">
                <div class="panel-heading">
                    <span class="step-number">03</span>
                    <div>
                        <h2>图表配置</h2>
                        <p>调整数据与视觉样式</p>
                    </div>
                </div>

                <div class="config-scroll">
                    <section class="config-group">
                        <h3>内容</h3>
                        <label class="field-label" for="chart-title">图表标题</label>
                        <el-input id="chart-title" v-model="chartTitle" maxlength="32" placeholder="输入标题" />

                        <label class="field-label spaced" for="data-source">数据源</label>
                        <el-select id="data-source" v-model="dataSource" class="full-width">
                            <el-option v-for="source in dataSources" :key="source.value" :label="source.label"
                                :value="source.value" />
                        </el-select>
                        <p class="field-hint">{{ datasetDescription }}</p>
                    </section>

                    <section class="config-group">
                        <h3>外观</h3>
                        <label class="field-label">主题</label>
                        <div class="theme-picker" role="group" aria-label="图表主题">
                            <button v-for="option in themes" :key="option.value" type="button" class="theme-option"
                                :class="[`swatch-${option.value}`, { selected: theme === option.value }]"
                                :aria-label="option.label" :aria-pressed="theme === option.value" :title="option.label"
                                @click="theme = option.value"><span></span></button>
                        </div>

                        <label class="field-label spaced">配色方案</label>
                        <div class="palette-list" role="group" aria-label="配色方案">
                            <button v-for="palette in palettes" :key="palette.value" type="button"
                                class="palette-option" :class="{ selected: paletteName === palette.value }"
                                :aria-pressed="paletteName === palette.value" @click="paletteName = palette.value">
                                <span class="palette-swatches">
                                    <i v-for="color in palette.colors.slice(0, 4)" :key="color"
                                        :style="{ backgroundColor: color }"></i>
                                </span>
                                <span>{{ palette.label }}</span>
                                <el-icon v-if="paletteName === palette.value">
                                    <Check />
                                </el-icon>
                            </button>
                        </div>

                        <label class="field-label spaced" for="series-color">主元素颜色</label>
                        <div class="color-control">
                            <input id="series-color" v-model="seriesColor" type="color" aria-label="选择主元素颜色" />
                            <code>{{ seriesColor.toUpperCase() }}</code>
                            <el-button text :icon="Refresh" aria-label="恢复当前方案主色" @click="resetSeriesColor" />
                        </div>

                        <template v-if="chartType === 'pie' || chartType === 'donut'">
                            <label class="field-label spaced" for="element-target">单项颜色</label>
                            <div class="color-control">
                                <el-select id="element-target" v-model="selectedElement" class="element-select">
                                    <el-option v-for="name in elementNames" :key="name" :label="name" :value="name" />
                                </el-select>
                                <input v-model="selectedElementColor" type="color" aria-label="设置当前数据项颜色" />
                            </div>
                        </template>
                    </section>

                    <section class="config-group config-toggles">
                        <h3>图表元素</h3>
                        <el-switch v-model="showLegend" active-text="显示图例" />
                        <el-switch v-model="showLabels" active-text="显示数值" />
                    </section>
                </div>
            </aside>
        </section>
    </main>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Component } from 'vue'
import type { EChartsOption } from 'echarts'
import { ElButton, ElIcon, ElInput, ElOption, ElSelect, ElSwitch, ElTag } from 'element-plus'
import {
    DataLine,
    Download,
    Histogram,
    PieChart,
    TrendCharts,
    Watermelon,
    Check,
    Refresh,
    RefreshLeft,
} from '@element-plus/icons-vue'
import vCommon from '@/components/v-common.vue'
import { useAiStore } from '@/stores/ai_item'
import { countryPopBar, worldPopulationLine } from '@/utils/mock_v1'

defineOptions({ name: 'ChartEditor' })

type ChartType = 'line' | 'area' | 'bar' | 'pie' | 'donut'
type DataSource = 'population' | 'countries' | 'ai-usage'
type ChartTheme = 'paper' | 'night' | 'westeros'

interface ChartDatum {
    name: string
    value: number
}

interface ChartTypeOption {
    value: ChartType
    label: string
    mark: string
    icon: Component
}

const chartTypes: ChartTypeOption[] = [
    { value: 'line', label: '折线图', mark: '01', icon: TrendCharts },
    { value: 'area', label: '面积图', mark: '02', icon: DataLine },
    { value: 'bar', label: '柱状图', mark: '03', icon: Histogram },
    { value: 'pie', label: '饼图', mark: '04', icon: PieChart },
    { value: 'donut', label: '环形图', mark: '05', icon: Watermelon },
]

const dataSources: { value: DataSource; label: string; description: string }[] = [
    { value: 'population', label: '全球人口趋势', description: '2015 至 2024 年全球人口数据，单位：百万。' },
    { value: 'countries', label: '国家人口排行', description: '各国家与地区人口对比数据，单位：百万。' },
    { value: 'ai-usage', label: 'AI 模型调用量', description: '来自当前 AI 使用数据状态，随数据变化更新。' },
]

const themes: { value: ChartTheme; label: string }[] = [
    { value: 'paper', label: '清透白' },
    { value: 'night', label: '午夜墨色' },
    { value: 'westeros', label: 'Westeros' },
]

const palettes = [
    { value: 'tidal', label: '潮汐', colors: ['#167d78', '#43aaa0', '#9acbb8', '#d7a66b', '#66849a', '#c9785c'] },
    { value: 'orchard', label: '果园', colors: ['#456d50', '#88a16c', '#d7a356', '#c56f52', '#836b91', '#5b91a0'] },
    { value: 'signal', label: '信号', colors: ['#2478a8', '#e17949', '#c6a23c', '#54a690', '#9366ad', '#d45f72'] },
]

const aiStore = useAiStore()
const chartType = ref<ChartType>('line')
const dataSource = ref<DataSource>('population')
const theme = ref<ChartTheme>('paper')
const paletteName = ref('tidal')
const chartTitle = ref('全球人口变化趋势')
const seriesColor = ref('#167d78')
const selectedElement = ref('')
const elementColors = ref<Record<string, string>>({})
const showLegend = ref(true)
const showLabels = ref(false)

const activePalette = computed(() => palettes.find((item) => item.value === paletteName.value) ?? palettes[0]!)

const dataset = computed<ChartDatum[]>(() => {
    if (dataSource.value === 'countries') {
        return countryPopBar.map((item) => ({ name: item.name, value: item.value }))
    }
    if (dataSource.value === 'ai-usage') {
        return aiStore.aiTable.map((item) => ({ name: item.ai_name, value: item.ai_use }))
    }
    return worldPopulationLine.map((item) => ({ name: item.year, value: item.pop }))
})

const selectedSource = computed(() => dataSources.find((item) => item.value === dataSource.value)!)
const datasetLabel = computed(() => selectedSource.value.label)
const datasetDescription = computed(() => selectedSource.value.description)
const activeChartLabel = computed(() => chartTypes.find((item) => item.value === chartType.value)!.label)
const seriesLabel = computed(() => dataSource.value === 'ai-usage' ? '模型调用量' : '人口数量')
const datasetTotal = computed(() => dataset.value.reduce((sum, item) => sum + item.value, 0))
const elementNames = computed(() => dataset.value.map((item) => item.name))
const formatNumber = (value: number): string => new Intl.NumberFormat('zh-CN').format(value)

watch([dataSource, chartType], () => {
    if (!elementNames.value.includes(selectedElement.value)) {
        selectedElement.value = elementNames.value[0] ?? ''
    }
})

watch(paletteName, () => {
    seriesColor.value = activePalette.value.colors[0]!
})

const selectedElementColor = computed({
    get: () => elementColors.value[selectedElement.value] ?? activePalette.value.colors[0]!,
    set: (color: string) => {
        if (selectedElement.value) elementColors.value[selectedElement.value] = color
    },
})

const chartOption = computed<EChartsOption>(() => {
    const dark = theme.value === 'night'
    const textColor = dark ? '#dce9e7' : '#52666a'
    const mutedColor = dark ? '#92a9a8' : '#87999a'
    const splitColor = dark ? 'rgba(169, 196, 191, 0.13)' : 'rgba(85, 120, 118, 0.13)'
    const pieData = dataset.value.map((item, index) => ({
        name: item.name,
        value: item.value,
        itemStyle: {
            color: elementColors.value[item.name]
                ?? activePalette.value.colors[index % activePalette.value.colors.length]
                ?? seriesColor.value,
        },
    }))
    const seriesType = chartType.value === 'area' ? 'line' : chartType.value === 'donut' ? 'pie' : chartType.value

    const sharedSeries = {
        name: seriesLabel.value,
        type: seriesType,
        data: chartType.value === 'pie' || chartType.value === 'donut'
            ? pieData
            : dataset.value.map((item) => ({
                name: item.name,
                value: item.value,
                itemStyle: { color: elementColors.value[item.name] ?? seriesColor.value },
            })),
        smooth: chartType.value === 'line' || chartType.value === 'area',
        symbol: 'circle',
        symbolSize: 7,
        barMaxWidth: 34,
        lineStyle: { color: seriesColor.value, width: 3 },
        itemStyle: { color: seriesColor.value, borderRadius: chartType.value === 'bar' ? [4, 4, 0, 0] : 0 },
        areaStyle: chartType.value === 'area' ? { opacity: 0.18, color: seriesColor.value } : undefined,
        radius: chartType.value === 'donut' ? ['46%', '72%'] : chartType.value === 'pie' ? '68%' : undefined,
        avoidLabelOverlap: true,
        label: {
            show: showLabels.value || chartType.value === 'pie' || chartType.value === 'donut',
            color: textColor,
            formatter: chartType.value === 'pie' || chartType.value === 'donut' ? '{b}  {d}%' : '{c}',
        },
        emphasis: { scale: true, scaleSize: 7 },
    }

    return {
        backgroundColor: 'transparent',
        color: activePalette.value.colors,
        animationDuration: 450,
        tooltip: {
            trigger: chartType.value === 'pie' || chartType.value === 'donut' ? 'item' : 'axis',
            backgroundColor: dark ? '#192827' : '#ffffff',
            borderColor: dark ? '#425b57' : '#dce6e2',
            textStyle: { color: textColor },
        },
        legend: {
            show: showLegend.value && (chartType.value === 'pie' || chartType.value === 'donut'),
            bottom: 0,
            textStyle: { color: mutedColor },
        },
        grid: { left: 58, right: 28, top: 30, bottom: chartType.value === 'pie' || chartType.value === 'donut' ? 56 : 44 },
        xAxis: chartType.value === 'pie' || chartType.value === 'donut' ? undefined : {
            type: 'category',
            data: dataset.value.map((item) => item.name),
            axisTick: { show: false },
            axisLine: { lineStyle: { color: splitColor } },
            axisLabel: { color: mutedColor, hideOverlap: true, rotate: dataSource.value === 'countries' ? 25 : 0 },
        },
        yAxis: chartType.value === 'pie' || chartType.value === 'donut' ? undefined : {
            type: 'value',
            axisLabel: { color: mutedColor },
            splitLine: { lineStyle: { color: splitColor, type: 'dashed' } },
        },
        series: [sharedSeries] as EChartsOption['series'],
    }
})

const resetSeriesColor = (): void => {
    seriesColor.value = activePalette.value.colors[0]!
    elementColors.value = {}
}

const resetConfig = (): void => {
    chartType.value = 'line'
    dataSource.value = 'population'
    theme.value = 'paper'
    paletteName.value = 'tidal'
    chartTitle.value = '全球人口变化趋势'
    seriesColor.value = palettes[0]!.colors[0]!
    elementColors.value = {}
    selectedElement.value = ''
    showLegend.value = true
    showLabels.value = false
}

const downloadConfig = (): void => {
    const serialized = JSON.stringify(chartOption.value, null, 2)
    const blob = new Blob([serialized], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'chart-option.json'
    anchor.click()
    URL.revokeObjectURL(url)
}
</script>

<style scoped lang="scss">
.chart-editor {
    --ink: #243331;
    --muted: #82918e;
    --line: #e2e9e5;
    --accent: #167d78;
    width: 100%;
    height: 100%;
    min-height: 560px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: #f2f5f2;
    color: var(--ink);
}

.editor-header {
    min-height: 72px;
    padding: 12px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    border-bottom: 1px solid var(--line);
    background: #fbfcfa;
}

.eyebrow {
    color: #6f8f87;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.25px;
}

.heading-copy h1 {
    margin-top: 2px;
    font-size: 19px;
    font-weight: 650;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 9px;
}

.save-state {
    margin-right: 8px;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    color: #73847f;
    font-size: 10px;
}

.save-state i {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4eac83;
}

.studio-layout {
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: 210px minmax(340px, 1fr) 310px;
}

.type-rail,
.config-panel {
    min-height: 0;
    display: flex;
    flex-direction: column;
    background: #fafbf9;
}

.type-rail {
    border-right: 1px solid var(--line);
}

.config-panel {
    border-left: 1px solid var(--line);
}

.rail-heading,
.panel-heading,
.preview-toolbar>div {
    min-height: 72px;
    padding: 15px 16px;
    display: flex;
    align-items: center;
    gap: 11px;
    border-bottom: 1px solid var(--line);
}

.step-number {
    color: #81a099;
    font-size: 10px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

.rail-heading h2,
.panel-heading h2,
.preview-toolbar h2 {
    font-size: 13px;
    font-weight: 650;
}

.rail-heading p,
.panel-heading p,
.preview-toolbar p {
    margin-top: 3px;
    color: var(--muted);
    font-size: 10px;
}

.chart-type-list {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.chart-type-option {
    min-height: 42px;
    padding: 0 10px;
    display: grid;
    grid-template-columns: 20px 1fr auto;
    align-items: center;
    gap: 9px;
    border: 1px solid transparent;
    border-radius: 4px;
    background: transparent;
    color: #586a66;
    cursor: pointer;
    text-align: left;
    transition: background-color 120ms ease, border-color 120ms ease, color 120ms ease;
}

.chart-type-option:hover {
    background: #f0f5f1;
}

.chart-type-option.selected {
    border-color: #c4ddd2;
    background: #e9f3ee;
    color: #216e60;
}

.chart-type-option>.el-icon {
    font-size: 16px;
}

.chart-type-option>span:nth-child(2) {
    font-size: 11px;
    font-weight: 550;
}

.type-mark {
    color: #a4b0ab;
    font-size: 9px;
    font-variant-numeric: tabular-nums;
}

.rail-footnote {
    margin-top: auto;
    padding: 13px 17px;
    border-top: 1px solid var(--line);
    color: #899691;
    font-size: 10px;
}

.rail-footnote span {
    color: var(--accent);
    font-weight: 700;
}

.preview-area {
    min-width: 0;
    min-height: 0;
    padding: 0 22px 18px;
    display: flex;
    flex-direction: column;
}

.preview-toolbar {
    min-height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--line);
}

.preview-toolbar>div {
    min-height: auto;
    padding: 0;
    border: 0;
}

.preview-frame {
    flex: 1;
    min-height: 280px;
    margin-top: 20px;
    padding: 20px 22px 14px;
    display: flex;
    flex-direction: column;
    border: 1px solid #e0e8e3;
    border-radius: 5px;
    background: #fff;
    transition: background-color 150ms ease, border-color 150ms ease;
}

.preview-frame.theme-night {
    border-color: #273c39;
    background: #12211f;
    color: #edf6f1;
}

.preview-frame.theme-westeros {
    border-color: #d5dce5;
    background: #f4f6f8;
}

.preview-chart-heading {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
    color: inherit;
    font-size: 14px;
    font-weight: 650;
}

.preview-chart-heading small {
    color: #95a29d;
    font-size: 10px;
    font-weight: 400;
}

.chart-canvas {
    flex: 1;
    min-height: 220px;
    margin-top: 12px;
}

.chart-canvas :deep(.common) {
    background: transparent;
}

.preview-footer {
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid rgba(125, 150, 139, 0.18);
    color: #899893;
    font-size: 9px;
}

.preview-footer span:first-child {
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.preview-footer i {
    width: 8px;
    height: 8px;
    border-radius: 2px;
}

.preview-caption {
    min-height: 42px;
    display: flex;
    align-items: center;
    gap: 9px;
    color: #889590;
    font-size: 10px;
}

.preview-caption strong {
    color: #536862;
    font-weight: 600;
}

.caption-divider {
    width: 1px;
    height: 13px;
    margin: 0 2px;
    background: #d7e0db;
}

.config-scroll {
    min-height: 0;
    overflow: auto;
}

.config-group {
    padding: 17px 16px 19px;
    border-bottom: 1px solid var(--line);
}

.config-group h3 {
    margin-bottom: 14px;
    color: #60726c;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.field-label {
    display: block;
    margin-bottom: 7px;
    color: #65746f;
    font-size: 10px;
}

.field-label.spaced {
    margin-top: 15px;
}

.full-width {
    width: 100%;
}

.field-hint {
    margin-top: 7px;
    color: #929e99;
    font-size: 9px;
    line-height: 1.5;
}

.theme-picker {
    display: flex;
    gap: 9px;
}

.theme-option {
    width: 44px;
    height: 34px;
    padding: 4px;
    border: 1px solid #dbe3de;
    border-radius: 4px;
    background: #fff;
    cursor: pointer;
}

.theme-option.selected {
    border-color: #368d76;
    box-shadow: 0 0 0 1px #368d76;
}

.theme-option span {
    width: 100%;
    height: 100%;
    display: block;
    border-radius: 2px;
}

.swatch-paper span {
    background: linear-gradient(135deg, #fff 50%, #dbe9e1 50%);
}

.swatch-night span {
    background: linear-gradient(135deg, #142522 50%, #284640 50%);
}

.swatch-westeros span {
    background: linear-gradient(135deg, #eff2f6 50%, #93b7e3 50%);
}

.palette-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.palette-option {
    min-height: 34px;
    padding: 4px 7px;
    display: flex;
    align-items: center;
    gap: 9px;
    border: 1px solid transparent;
    border-radius: 4px;
    background: transparent;
    color: #5d6d68;
    cursor: pointer;
    text-align: left;
}

.palette-option.selected {
    border-color: #d4e6dc;
    background: #edf5ef;
    color: #356d5e;
}

.palette-option>span:nth-child(2) {
    flex: 1;
    font-size: 10px;
}

.palette-swatches {
    display: flex;
    gap: 3px;
}

.palette-swatches i {
    width: 13px;
    height: 13px;
    border-radius: 3px;
}

.palette-option>.el-icon {
    color: var(--accent);
}

.color-control {
    min-height: 34px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.color-control input[type='color'] {
    width: 32px;
    height: 30px;
    padding: 2px;
    border: 1px solid #dbe3de;
    border-radius: 4px;
    background: #fff;
    cursor: pointer;
}

.color-control code {
    flex: 1;
    color: #70817a;
    font-size: 10px;
}

.color-control :deep(.el-button) {
    color: #788982;
}

.element-select {
    flex: 1;
    min-width: 0;
}

.config-toggles {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 13px;
}

.config-toggles h3 {
    margin-bottom: 0;
}

.config-toggles :deep(.el-switch) {
    --el-switch-on-color: #438b77;
}

@media (max-width: 1050px) {
    .studio-layout {
        grid-template-columns: 176px minmax(300px, 1fr) 280px;
    }

    .preview-area {
        padding-inline: 16px;
    }
}

@media (max-width: 820px) {
    .chart-editor {
        height: auto;
        min-height: 100%;
        overflow: auto;
    }

    .editor-header {
        align-items: flex-start;
        flex-direction: column;
        padding: 14px 16px;
    }

    .header-actions {
        width: 100%;
        flex-wrap: wrap;
    }

    .save-state {
        margin-right: auto;
    }

    .studio-layout {
        grid-template-columns: minmax(0, 1fr);
    }

    .type-rail {
        border-right: 0;
        border-bottom: 1px solid var(--line);
    }

    .rail-heading {
        min-height: 54px;
        border-bottom: 0;
    }

    .chart-type-list {
        padding: 0 12px 12px;
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 5px;
    }

    .chart-type-option {
        min-height: 56px;
        padding: 7px 4px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 4px;
        text-align: center;
    }

    .chart-type-option>span:nth-child(2) {
        font-size: 9px;
    }

    .type-mark,
    .rail-footnote {
        display: none;
    }

    .preview-area {
        min-height: 440px;
        padding: 0 14px 12px;
    }

    .preview-toolbar {
        min-height: 58px;
    }

    .preview-frame {
        min-height: 330px;
        margin-top: 12px;
        padding: 15px;
    }

    .config-panel {
        border-top: 1px solid var(--line);
        border-left: 0;
    }

    .panel-heading {
        min-height: 58px;
    }

    .config-scroll {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .config-group {
        border-right: 1px solid var(--line);
    }
}

@media (max-width: 520px) {
    .heading-copy h1 {
        font-size: 17px;
    }

    .header-actions :deep(.el-button) {
        padding: 8px 10px;
        font-size: 10px;
    }

    .chart-type-list {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .config-scroll {
        grid-template-columns: minmax(0, 1fr);
    }

    .config-group {
        border-right: 0;
    }
}
</style>