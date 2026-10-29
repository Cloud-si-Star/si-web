<template>
    <main class="con-page alone-set">
        <section class="page-header">
            <div>
                <p class="eyebrow">SALES DATA PIPELINE</p>
                <h1>销售数据处理</h1>
                <p class="page-description">按业务日期执行销售数据分层处理，并查看每次执行结果。</p>
                <div class="section-heading">
                    <div>
                        <h2>处理流程</h2>
                        <p>日期按接口要求自动校验：日任务使用 YYYYMMDD，月度任务使用 YYYYMM。</p>
                    </div>
                    <el-tag type="info" effect="plain">{{ tasks.length }} 项操作</el-tag>
                </div>
            </div>
            <div class="header-mark">
                <el-icon>
                    <TrendCharts />
                </el-icon>
            </div>
        </section>

        <section class="pipeline-section" style="flex:1">


            <el-table :data="tasks" row-key="key" border class="task-table" empty-text="暂无处理任务" style="height: 100%;">
                <el-table-column label="处理任务" min-width="205">
                    <template #default="{ row }">
                        <div class="task-title">
                            <span class="task-icon" :class="`tone-${row.color}`">
                                <el-icon>
                                    <component :is="row.icon" />
                                </el-icon>
                            </span>
                            <div>
                                <strong>{{ row.name }}</strong>
                                <span class="task-layer">{{ row.layer }}</span>
                            </div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="description" label="说明" min-width="260" show-overflow-tooltip />
                <el-table-column label="业务日期" width="205" align="center">
                    <template #default="{ row }">
                        <template v-if="row.dateFormat === 'day'">
                            <el-date-picker v-model="dailyBizDate" type="date" format="YYYY-MM-DD"
                                value-format="YYYYMMDD" :clearable="false" :disabled="runningKeys.has(row.key)"
                                placeholder="选择业务日期" />
                        </template>
                        <template v-else-if="row.dateFormat === 'month'">
                            <el-date-picker v-model="monthlyBizDate" type="month" format="YYYY-MM" value-format="YYYYMM"
                                :clearable="false" :disabled="runningKeys.has(row.key)" placeholder="选择业务月份" />
                        </template>
                        <span v-else class="not-required">无需选择</span>
                    </template>
                </el-table-column>
                <el-table-column label="最近执行" min-width="220">
                    <template #default="{ row }">
                        <div v-if="results[row.key]" class="result-cell">
                            <el-tag :type="resultTagType(results[row.key]!.status)" size="small" effect="light">
                                {{ resultStatusLabel(results[row.key]!.status) }}
                            </el-tag>
                            <span class="result-message" :title="results[row.key]!.message">
                                {{ results[row.key]!.message }}
                            </span>
                            <small>{{ results[row.key]!.finishedAt }}</small>
                        </div>
                        <span v-else class="no-result">尚未执行</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="145" fixed="right" align="center">
                    <template #default="{ row }">
                        <el-button :type="row.key === 'seed' ? 'warning' : 'primary'"
                            :icon="row.key === 'seed' ? Warning : VideoPlay" :loading="runningKeys.has(row.key)"
                            :disabled="runningKeys.size > 0" @click="handleRun(row.key)">
                            {{ runningKeys.has(row.key) ? '执行中' : row.buttonLabel }}
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <footer class="pipeline-footer">
                <span class="footer-dot"></span>
                执行结果仅保存在当前页面；后端当前以同步方式处理，接口返回后显示本次统计结果。
            </footer>
        </section>

        <el-dialog v-model="seedConfirmVisible" title="确认生成销售种子数据" width="460px">
            <div class="confirm-content">
                <el-icon>
                    <WarningFilled />
                </el-icon>
                <p>
                    该接口会生成约 21 个月的演示日期、区域、商品及销售事实数据。
                    重复执行可能产生重复数据，请确认目标数据库允许写入后再继续。
                </p>
            </div>
            <template #footer>
                <el-button @click="seedConfirmVisible = false">取消</el-button>
                <el-button type="warning" :loading="runningKeys.has('seed')" @click="confirmSeed">
                    确认执行
                </el-button>
            </template>
        </el-dialog>
    </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
    ElAlert,
    ElButton,
    ElDatePicker,
    ElDialog,
    ElIcon,
    ElMessage,
    ElTable,
    ElTableColumn,
    ElTag,
} from 'element-plus'
import {
    Calendar,
    Collection,
    DataAnalysis,
    Files,
    Histogram,
    TrendCharts,
    VideoPlay,
    Warning,
    WarningFilled,
} from '@element-plus/icons-vue'
import { boardApi, type SalesTask, type TaskResult, type TaskRunStatus } from './type'

defineOptions({ name: 'SalesDataPipeline' })

const today = new Date()
const dailyBizDate = ref(
    `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`,
)
const monthlyBizDate = ref(`${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}`)
const runningKeys = ref(new Set<string>())
const results = ref<Record<string, TaskResult>>({})
const seedConfirmVisible = ref(false)

const tasks: SalesTask[] = [
    {
        key: 'seed',
        name: '生成销售种子数据',
        layer: '演示数据初始化',
        description: '生成日期、区域、商品维度及销售事实数据',
        dateFormat: 'none',
        buttonLabel: '生成数据',
        color: 'orange',
        icon: Collection,
    },
    {
        key: 'ods',
        name: '贴源层数据抽取',
        layer: 'ODS',
        description: '从销售事实数据抽取指定日期的贴源层数据',
        dateFormat: 'day',
        buttonLabel: '执行 ODS',
        color: 'blue',
        icon: Files,
    },
    {
        key: 'dwd',
        name: '数据仓库明细加工',
        layer: 'DWD',
        description: '加工指定日期的销售明细及数据质量信息',
        dateFormat: 'day',
        buttonLabel: '执行 DWD',
        color: 'purple',
        icon: DataAnalysis,
    },
    {
        key: 'daily',
        name: '日销量汇总',
        layer: 'DWS · 日',
        description: '按业务日期汇总销售指标',
        dateFormat: 'day',
        buttonLabel: '执行日汇总',
        color: 'green',
        icon: Calendar,
    },
    {
        key: 'daily-category',
        name: '日销量品类汇总',
        layer: 'DWS · 日 × 品类',
        description: '按业务日期及商品大类汇总销售指标',
        dateFormat: 'day',
        buttonLabel: '执行品类汇总',
        color: 'teal',
        icon: Histogram,
    },
    {
        key: 'monthly-region',
        name: '月度区域汇总',
        layer: 'DWS · 月 × 大区',
        description: '按月份汇总各大区销售指标',
        dateFormat: 'month',
        buttonLabel: '执行月汇总',
        color: 'indigo',
        icon: TrendCharts,
    },
]

async function handleRun(taskKey: string): Promise<void> {
    const task = tasks.find((item) => item.key === taskKey)
    if (!task) {
        ElMessage.error('未找到销售数据处理任务')
        return
    }

    if (task.key === 'seed') {
        seedConfirmVisible.value = true
        return
    }
    await runTask(task)
}

async function confirmSeed(): Promise<void> {
    const seedTask = tasks.find((task) => task.key === 'seed')
    if (!seedTask) {
        ElMessage.error('未找到种子数据任务配置')
        return
    }

    seedConfirmVisible.value = false
    await runTask(seedTask)
}

async function runTask(task: SalesTask): Promise<void> {
    runningKeys.value = new Set(runningKeys.value).add(task.key)
    results.value = {
        ...results.value,
        [task.key]: {
            status: 'running',
            message: '请求已发送，等待后端处理完成',
            finishedAt: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
        },
    }

    try {
        const response = await boardApi.run(task.key, {
            dailyBizDate: dailyBizDate.value,
            monthlyBizDate: monthlyBizDate.value,
        })
        let message: string
        if (task.key === 'seed') {
            message = '种子数据生成接口执行成功'
        } else if (response) {
            message = `业务日期 ${response.bizDate}，插入 ${response.insertTotal} 条，丢弃 ${response.dropCount} 条`
        } else {
            throw new Error('后端未返回处理统计结果')
        }

        setResult(task.key, 'success', message)
        ElMessage.success(`${task.name}执行成功`)
    } catch (error) {
        const message = error instanceof Error ? error.message : `${task.name}执行失败`
        setResult(task.key, 'failed', message)
        ElMessage.error(message)
    } finally {
        const nextRunningKeys = new Set(runningKeys.value)
        nextRunningKeys.delete(task.key)
        runningKeys.value = nextRunningKeys
    }
}

function setResult(key: string, status: TaskRunStatus, message: string): void {
    results.value = {
        ...results.value,
        [key]: {
            status,
            message,
            finishedAt: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
        },
    }
}

function resultStatusLabel(status: TaskRunStatus): string {
    const labels: Record<TaskRunStatus, string> = {
        running: '处理中',
        success: '成功',
        failed: '失败',
    }
    return labels[status]
}

function resultTagType(status: TaskRunStatus): 'warning' | 'success' | 'danger' {
    const types: Record<TaskRunStatus, 'warning' | 'success' | 'danger'> = {
        running: 'warning',
        success: 'success',
        failed: 'danger',
    }
    return types[status]
}
</script>

<style lang="scss" scoped>
.alone-set {
    flex-direction: column;
    gap: 12px;
}

.page-header,
.pipeline-section {
    border: 1px solid #e8edf3;
    border-radius: 12px;
    background: #fff;
    box-shadow: 0 5px 18px rgb(25 55 90 / 4%);
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 26px;
}

.eyebrow {
    margin: 0 0 7px;
    color: #5685bd;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.page-header h1 {
    margin: 0;
    color: #253950;
    font-size: 23px;
    font-weight: 650;
}

.page-description {
    margin: 8px 0 0;
    color: #8290a0;
    font-size: 13px;
}

.header-mark {
    display: grid;
    width: 52px;
    height: 52px;
    place-items: center;
    border-radius: 14px;
    background: #edf5ff;
    color: #5b8dcc;
    font-size: 25px;
}

.seed-warning {
    border-radius: 9px;
}

.pipeline-section {
    padding: 22px 22px 0;
    overflow: hidden;
}

.section-heading {
    display: none;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 18px;
}

.section-heading h2 {
    margin: 0;
    color: #2b3e54;
    font-size: 17px;
}

.section-heading p {
    margin: 7px 0 0;
    color: #8a98a8;
    font-size: 12px;
}

.task-table {
    width: 100%;
}

.task-title {
    display: flex;
    align-items: center;
    gap: 11px;
}

.task-icon {
    display: grid;
    width: 36px;
    height: 36px;
    flex: 0 0 auto;
    place-items: center;
    border-radius: 10px;
    font-size: 17px;
}

.tone-orange {
    background: #fff5e9;
    color: #d9973e;
}

.tone-blue {
    background: #edf5ff;
    color: #578bcc;
}

.tone-purple {
    background: #f3efff;
    color: #8b72cd;
}

.tone-green {
    background: #eaf8f1;
    color: #51a77c;
}

.tone-teal {
    background: #e8f8f6;
    color: #43a69c;
}

.tone-indigo {
    background: #eef0ff;
    color: #6775c8;
}

.task-title strong,
.task-layer {
    display: block;
}

.task-title strong {
    color: #34495f;
    font-size: 13px;
    font-weight: 600;
}

.task-layer {
    margin-top: 5px;
    color: #9aa6b3;
    font-size: 11px;
}

.not-required,
.no-result {
    color: #a0acb9;
    font-size: 12px;
}

.result-cell {
    display: grid;
    grid-template-columns: max-content minmax(0, 1fr);
    align-items: center;
    gap: 5px 8px;
}

.result-message {
    overflow: hidden;
    color: #64758a;
    font-size: 12px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.result-cell small {
    grid-column: 2;
    color: #9ba7b4;
    font-size: 10px;
}

.pipeline-footer {
    display: flex;
    align-items: center;
    gap: 8px;
    min-height: 48px;
    color: #95a1ae;
    font-size: 12px;
}

.footer-dot {
    width: 7px;
    height: 7px;
    flex: 0 0 auto;
    border-radius: 50%;
    background: #5993ce;
}

.confirm-content {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    color: #657487;
    line-height: 1.7;
}

.confirm-content .el-icon {
    flex: 0 0 auto;
    margin-top: 3px;
    color: #d99a3f;
    font-size: 20px;
}

.confirm-content p {
    margin: 0;
}

@media (max-width: 700px) {
    .sales-etl-page {
        gap: 12px;
        padding: 0;
    }

    .page-header {
        padding: 18px;
    }

    .header-mark {
        width: 42px;
        height: 42px;
        font-size: 21px;
    }

    .pipeline-section {
        padding: 17px 12px 0;
    }

    .section-heading {
        align-items: flex-start;
    }
}
</style>
