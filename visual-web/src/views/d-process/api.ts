import { request } from '@/utils/request'

export type ProcessStatus = 'idle' | 'running' | 'success' | 'failed'

export interface DataProcess {
    id: string
    name: string
    description: string
    source: string
    status: ProcessStatus
    progress: number
    processed: number
    total: number
    triggeredBy: string
    startedAt: string | null
    finishedAt: string | null
    elapsedSeconds: number
    message: string
}

interface MockProcess extends DataProcess {
    runStartedAt: number | null
    durationMs: number
}

const USE_MOCK_DATA = true

const mockProcesses: MockProcess[] = [
    {
        id: 'sales-daily',
        name: '销售数据清洗入库',
        description: '清洗销售明细并写入业务数据库',
        source: 'sales_raw',
        status: 'success',
        progress: 100,
        processed: 12864,
        total: 12864,
        triggeredBy: '系统示例',
        startedAt: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
        finishedAt: new Date(Date.now() - 58 * 60 * 1000).toISOString(),
        elapsedSeconds: 120,
        message: '处理完成，数据已入库',
        runStartedAt: null,
        durationMs: 90_000,
    },
    {
        id: 'customer-sync',
        name: '客户资料同步',
        description: '校验客户资料并同步至客户数据表',
        source: 'customer_source',
        status: 'idle',
        progress: 0,
        processed: 0,
        total: 8360,
        triggeredBy: '--',
        startedAt: null,
        finishedAt: null,
        elapsedSeconds: 0,
        message: '等待触发',
        runStartedAt: null,
        durationMs: 120_000,
    },
    {
        id: 'inventory-summary',
        name: '库存汇总计算',
        description: '汇总仓库库存并更新库存统计表',
        source: 'inventory_raw',
        status: 'success',
        progress: 100,
        processed: 5620,
        total: 5620,
        triggeredBy: '系统示例',
        startedAt: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
        finishedAt: new Date(Date.now() - 3 * 60 * 60 * 1000 + 75_000).toISOString(),
        elapsedSeconds: 75,
        message: '处理完成，数据已入库',
        runStartedAt: null,
        durationMs: 90_000,
    },
    {
        id: 'event-import',
        name: '用户事件导入',
        description: '导入并整理用户行为事件记录',
        source: 'user_event_source',
        status: 'idle',
        progress: 0,
        processed: 0,
        total: 24150,
        triggeredBy: '--',
        startedAt: null,
        finishedAt: null,
        elapsedSeconds: 0,
        message: '等待触发',
        runStartedAt: null,
        durationMs: 150_000,
    },
]

function updateMockProgress(process: MockProcess, now = Date.now()): void {
    if (process.status !== 'running' || process.runStartedAt === null) return

    const elapsedMs = now - process.runStartedAt
    process.elapsedSeconds = Math.floor(elapsedMs / 1000)
    process.progress = Math.min(99, Math.floor((elapsedMs / process.durationMs) * 100))
    process.processed = Math.floor((process.total * process.progress) / 100)

    if (elapsedMs >= process.durationMs) {
        process.status = 'success'
        process.progress = 100
        process.processed = process.total
        process.finishedAt = new Date(now).toISOString()
        process.elapsedSeconds = Math.floor(process.durationMs / 1000)
        process.message = '处理完成，数据已入库'
        process.runStartedAt = null
    }
}

function toDataProcess(process: MockProcess): DataProcess {
    const { runStartedAt: _runStartedAt, durationMs: _durationMs, ...data } = process
    return { ...data }
}

export const dataProcessApi = {
    /** 获取数据处理任务及其最近一次运行状态。 */
    async getProcesses(): Promise<DataProcess[]> {
        if (!USE_MOCK_DATA) {
            return request.get<DataProcess[]>('/v1/data-process/processes')
        }

        const now = Date.now()
        mockProcesses.forEach((process) => updateMockProgress(process, now))
        return mockProcesses.map(toDataProcess)
    },

    /** 触发指定数据处理任务；真实接口就绪后关闭模拟数据开关即可切换。 */
    async startProcess(processId: string): Promise<DataProcess> {
        if (!USE_MOCK_DATA) {
            return request.post<DataProcess>(`/v1/data-process/processes/${processId}/runs`)
        }

        const process = mockProcesses.find((item) => item.id === processId)
        if (!process) {
            throw new Error('未找到要处理的数据任务')
        }
        if (process.status === 'running') {
            throw new Error('该任务正在处理中，请勿重复触发')
        }

        const now = Date.now()
        process.status = 'running'
        process.progress = 0
        process.processed = 0
        process.triggeredBy = '当前用户'
        process.startedAt = new Date(now).toISOString()
        process.finishedAt = null
        process.elapsedSeconds = 0
        process.message = '正在处理数据，请稍候'
        process.runStartedAt = now

        return toDataProcess(process)
    },
}
