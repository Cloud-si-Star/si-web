<template>
    <main class="process-page">
        <section class="overview">
            <div class="page-heading">
                <p class="eyebrow">DATA PIPELINE WORKSPACE</p>
                <h1>数据处理任务</h1>
                <p>触发后台数据处理任务，并定时查看数据入库进度。</p>
            </div>

            <div class="overview-card">
                <span>处理任务</span>
                <strong>{{ processes.length }}</strong>
                <small>当前任务总数</small>
            </div>
            <div class="overview-card">
                <span>处理中</span>
                <strong class="running-count">{{ runningCount }}</strong>
                <small>后台运行任务</small>
            </div>
            <div class="overview-card">
                <span>已完成</span>
                <strong class="success-count">{{ completedCount }}</strong>
                <small>最近运行成功</small>
            </div>
        </section>

        <section class="task-section">
            <div class="section-heading">
                <div>
                    <div class="section-title">
                        <el-icon class="title-icon"><DataLine /></el-icon>
                        <h2>处理任务列表</h2>
                    </div>
                    <p>长耗时任务将在后台执行；页面每 30 秒查询一次运行进度。</p>
                </div>
                <div class="heading-actions">
                    <span class="updated-at">
                        <el-icon><Clock /></el-icon>
                        {{ lastUpdatedAt ? `最近更新 ${lastUpdatedAt}` : '尚未获取任务状态' }}
                    </span>
                    <el-button :icon="Refresh" :loading="loading" @click="loadProcesses()">刷新状态</el-button>
                </div>
            </div>

            <el-alert v-if="runningCount > 0" class="polling-alert" type="info" :closable="false" show-icon>
                <template #title>
                    任务正在处理中，页面会自动刷新进度；所有任务完成后将停止轮询。
                </template>
            </el-alert>

            <el-table v-loading="loading" :data="processes" row-key="id" border class="process-table"
                empty-text="暂无数据处理任务">
                <el-table-column prop="name" label="处理任务" min-width="170">
                    <template #default="{ row }">
                        <div class="task-name">{{ row.name }}</div>
                        <div class="task-description">{{ row.description }}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="source" label="数据来源" min-width="145" show-overflow-tooltip />
                <el-table-column label="处理进度" min-width="230">
                    <template #default="{ row }">
                        <div class="progress-cell">
                            <div class="progress-heading">
                                <span>{{ progressLabel(row.status) }}</span>
                                <strong>{{ row.progress }}%</strong>
                            </div>
                            <el-progress :percentage="row.progress" :stroke-width="8"
                                :status="row.status === 'success' ? 'success' : undefined" :show-text="false" />
                            <span class="processed-count">
                                {{ formatNumber(row.processed) }} / {{ formatNumber(row.total) }} 条
                            </span>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="状态" width="110" align="center">
                    <template #default="{ row }">
                        <el-tag :type="statusTagType(row.status)" effect="light">
                            {{ statusLabel(row.status) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="triggeredBy" label="触发人" width="110" align="center" />
                <el-table-column label="开始时间" min-width="175">
                    <template #default="{ row }">
                        {{ formatDate(row.startedAt) }}
                    </template>
                </el-table-column>
                <el-table-column label="耗时" width="95" align="center">
                    <template #default="{ row }">
                        {{ formatDuration(row.elapsedSeconds) }}
                    </template>
                </el-table-column>
                <el-table-column label="最近结果" min-width="180" show-overflow-tooltip>
                    <template #default="{ row }">
                        <span :class="{ 'result-error': row.status === 'failed' }">{{ row.message }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="145" fixed="right" align="center">
                    <template #default="{ row }">
                        <el-button type="primary" :icon="VideoPlay" :loading="startingIds.has(row.id)"
                            :disabled="row.status === 'running'" @click="startProcess(row.id)">
                            {{ triggerLabel(row.status) }}
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <footer class="section-footer">
                <span class="mock-indicator"></span>
                当前为前端模拟数据，后端接口就绪后可在任务 API 文件中切换为真实请求。
            </footer>
        </section>
    </main>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import {
    ElAlert,
    ElButton,
    ElIcon,
    ElProgress,
    ElTable,
    ElTableColumn,
    ElTag,
    ElMessage,
} from 'element-plus'
import { Clock, DataLine, Refresh, VideoPlay } from '@element-plus/icons-vue'
import { dataProcessApi, type DataProcess, type ProcessStatus } from './api'

defineOptions({ name: 'DataProcessPage' })

const POLLING_INTERVAL = 30_000

const processes = ref<DataProcess[]>([])
const loading = ref(false)
const startingIds = ref(new Set<string>())
const lastUpdatedAt = ref('')
let pollingTimer: ReturnType<typeof setTimeout> | undefined

const runningCount = computed(() => processes.value.filter((item) => item.status === 'running').length)
const completedCount = computed(() => processes.value.filter((item) => item.status === 'success').length)

function clearPolling(): void {
    if (pollingTimer !== undefined) {
        clearTimeout(pollingTimer)
        pollingTimer = undefined
    }
}

function schedulePolling(): void {
    clearPolling()
    if (runningCount.value === 0) return

    pollingTimer = setTimeout(async () => {
        pollingTimer = undefined
        await loadProcesses()
    }, POLLING_INTERVAL)
}

async function loadProcesses(): Promise<void> {
    loading.value = true
    try {
        processes.value = await dataProcessApi.getProcesses()
        lastUpdatedAt.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
    } catch (error) {
        ElMessage.error(error instanceof Error ? error.message : '数据处理任务加载失败')
    } finally {
        loading.value = false
        schedulePolling()
    }
}

async function startProcess(processId: string): Promise<void> {
    const process = processes.value.find((item) => item.id === processId)
    if (!process) {
        ElMessage.error('未找到要处理的数据任务')
        return
    }

    startingIds.value = new Set(startingIds.value).add(process.id)
    try {
        const startedProcess = await dataProcessApi.startProcess(process.id)
        processes.value = processes.value.map((item) => item.id === startedProcess.id ? startedProcess : item)
        lastUpdatedAt.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
        ElMessage.success(`${process.name}已开始处理`)
        schedulePolling()
    } catch (error) {
        ElMessage.error(error instanceof Error ? error.message : '触发数据处理任务失败')
    } finally {
        const nextStartingIds = new Set(startingIds.value)
        nextStartingIds.delete(process.id)
        startingIds.value = nextStartingIds
    }
}

function statusLabel(status: ProcessStatus): string {
    const labels: Record<ProcessStatus, string> = {
        idle: '待处理',
        running: '处理中',
        success: '已完成',
        failed: '处理失败',
    }
    return labels[status]
}

function statusTagType(status: ProcessStatus): 'info' | 'warning' | 'success' | 'danger' {
    const types: Record<ProcessStatus, 'info' | 'warning' | 'success' | 'danger'> = {
        idle: 'info',
        running: 'warning',
        success: 'success',
        failed: 'danger',
    }
    return types[status]
}

function triggerLabel(status: ProcessStatus): string {
    if (status === 'running') return '处理中'
    if (status === 'success') return '重新处理'
    if (status === 'failed') return '重试'
    return '开始处理'
}

function progressLabel(status: ProcessStatus): string {
    if (status === 'idle') return '等待开始'
    if (status === 'running') return '正在处理数据'
    return status === 'success' ? '入库完成' : '处理未完成'
}

function formatNumber(value: number): string {
    return new Intl.NumberFormat('zh-CN').format(value)
}

function formatDate(value: string | null): string {
    return value ? new Date(value).toLocaleString('zh-CN', { hour12: false }) : '--'
}

function formatDuration(seconds: number): string {
    if (seconds < 60) return `${seconds} 秒`
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return remainingSeconds === 0 ? `${minutes} 分钟` : `${minutes} 分 ${remainingSeconds} 秒`
}

onMounted(() => {
    void loadProcesses()
})

onUnmounted(() => {
    clearPolling()
})
</script>

<style scoped>
.process-page {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 100%;
    padding: 4px;
    color: #263445;
}

.overview {
    display: grid;
    grid-template-columns: minmax(280px, 1.8fr) repeat(3, minmax(150px, 1fr));
    gap: 14px;
}

.page-heading,
.overview-card,
.task-section {
    border: 1px solid #e8edf3;
    border-radius: 12px;
    background: #fff;
    box-shadow: 0 5px 18px rgb(25 55 90 / 4%);
}

.page-heading {
    padding: 21px 24px;
}

.eyebrow {
    margin: 0 0 8px;
    color: #5287c7;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.page-heading h1 {
    margin: 0;
    color: #24364b;
    font-size: 23px;
    font-weight: 650;
}

.page-heading > p:last-child {
    margin: 8px 0 0;
    color: #8190a2;
    font-size: 13px;
}

.overview-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 18px 20px;
}

.overview-card span {
    color: #7c8b9d;
    font-size: 13px;
}

.overview-card strong {
    margin: 8px 0 4px;
    color: #273c54;
    font-size: 27px;
    line-height: 1;
}

.overview-card strong.running-count {
    color: #d9902f;
}

.overview-card strong.success-count {
    color: #40a77a;
}

.overview-card small {
    color: #a0adba;
    font-size: 12px;
}

.task-section {
    padding: 22px 22px 0;
    overflow: hidden;
}

.section-heading,
.heading-actions,
.section-title {
    display: flex;
    align-items: center;
}

.section-heading {
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 18px;
}

.section-title {
    gap: 9px;
}

.section-title h2 {
    margin: 0;
    color: #293c52;
    font-size: 17px;
}

.title-icon {
    color: #5789c5;
    font-size: 19px;
}

.section-heading p {
    margin: 7px 0 0 28px;
    color: #8997a7;
    font-size: 12px;
}

.heading-actions {
    flex-shrink: 0;
    gap: 14px;
}

.updated-at {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #8b98a7;
    font-size: 12px;
}

.polling-alert {
    margin-bottom: 14px;
}

.process-table {
    width: 100%;
}

.task-name {
    color: #33485f;
    font-weight: 600;
}

.task-description {
    margin-top: 5px;
    color: #98a4b1;
    font-size: 12px;
    line-height: 1.5;
}

.progress-cell {
    min-width: 150px;
}

.progress-heading {
    display: flex;
    justify-content: space-between;
    margin-bottom: 7px;
    color: #78889a;
    font-size: 12px;
}

.progress-heading strong {
    color: #425b76;
    font-weight: 600;
}

.processed-count {
    display: block;
    margin-top: 5px;
    color: #9aa6b3;
    font-size: 11px;
}

.result-error {
    color: #d65b5b;
}

.section-footer {
    display: flex;
    align-items: center;
    gap: 8px;
    min-height: 48px;
    color: #95a1ae;
    font-size: 12px;
}

.mock-indicator {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #dba34b;
}

@media (max-width: 1000px) {
    .overview {
        grid-template-columns: repeat(3, minmax(130px, 1fr));
    }

    .page-heading {
        grid-column: 1 / -1;
    }

    .section-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .heading-actions {
        width: 100%;
        justify-content: space-between;
    }
}

@media (max-width: 600px) {
    .process-page {
        gap: 12px;
        padding: 0;
    }

    .overview {
        gap: 8px;
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .page-heading {
        padding: 17px;
    }

    .overview-card {
        padding: 14px 12px;
    }

    .overview-card strong {
        font-size: 23px;
    }

    .overview-card small {
        font-size: 10px;
    }

    .task-section {
        padding: 17px 12px 0;
    }

    .heading-actions {
        align-items: flex-start;
        flex-direction: column;
    }
}
</style>
