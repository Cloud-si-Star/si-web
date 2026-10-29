import { request } from '@/utils/request'
import type { Component } from 'vue'

export type SalesTaskKey = 'seed' | 'ods' | 'dwd' | 'daily' | 'daily-category' | 'monthly-region'
export type TaskRunStatus = 'running' | 'success' | 'failed'
export type TaskDateFormat = 'none' | 'day' | 'month'

export interface SalesTask {
    key: SalesTaskKey
    name: string
    layer: string
    description: string
    dateFormat: TaskDateFormat
    buttonLabel: string
    color: string
    icon: Component
}

export interface SalesTaskDates {
    dailyBizDate: string
    monthlyBizDate: string
}

export interface SalesEtlResult {
    bizDate: string
    insertTotal: number
    dropCount: number
    actConut: number
}

export interface TaskResult {
    status: TaskRunStatus
    message: string
    finishedAt: string
}

const SALES_API = '/v1/sales'
const SALES_REQUEST_TIMEOUT = 10 * 60 * 1000

function assertBizDate(value: string): void {
    if (!/^\d{8}$/.test(value)) {
        throw new Error('业务日期格式错误，请选择 YYYYMMDD 格式的日期')
    }

    const year = Number(value.slice(0, 4))
    const month = Number(value.slice(4, 6))
    const day = Number(value.slice(6, 8))
    const date = new Date(year, month - 1, day)
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
        throw new Error('业务日期无效，请选择真实存在的日期')
    }
}

function assertBizMonth(value: string): void {
    if (!/^\d{6}$/.test(value)) {
        throw new Error('业务月份格式错误，请选择 YYYYMM 格式的月份')
    }

    const month = Number(value.slice(4, 6))
    if (month < 1 || month > 12) {
        throw new Error('业务月份无效，请选择 01 至 12 月')
    }
}

function postForBizDate(path: string, bizdate: string): Promise<SalesEtlResult> {
    assertBizDate(bizdate)
    return request.post<SalesEtlResult>(`${SALES_API}/${path}`, undefined, {
        params: { bizdate },
        timeout: SALES_REQUEST_TIMEOUT,
    })
}

export const boardApi = {
    /** POST /v1/sales/seeds：生成固定日期范围的销售演示数据。 */
    createSeedData(): Promise<null> {
        return request.post<null>(`${SALES_API}/seeds`, undefined, {
            timeout: SALES_REQUEST_TIMEOUT,
        })
    },

    /** POST /v1/sales/ods-sales?bizdate=YYYYMMDD：执行 ODS 数据抽取。 */
    runOdsSales(bizdate: string): Promise<SalesEtlResult> {
        return postForBizDate('ods-sales', bizdate)
    },

    /** POST /v1/sales/dwd-sales-detail?bizdate=YYYYMMDD：执行 DWD 明细加工。 */
    runDwdSalesDetail(bizdate: string): Promise<SalesEtlResult> {
        return postForBizDate('dwd-sales-detail', bizdate)
    },

    /** POST /v1/sales/dws-sales-daily?bizdate=YYYYMMDD：执行日销量汇总。 */
    runDailySales(bizdate: string): Promise<SalesEtlResult> {
        return postForBizDate('dws-sales-daily', bizdate)
    },

    /** POST /v1/sales/dws-sales-daily-category?bizdate=YYYYMMDD：执行日品类汇总。 */
    runDailyCategorySales(bizdate: string): Promise<SalesEtlResult> {
        return postForBizDate('dws-sales-daily-category', bizdate)
    },

    /** POST /v1/sales/dws-sales-monthly-region?bizdate=YYYYMM：执行月度区域汇总。 */
    runMonthlyRegionSales(bizdate: string): Promise<SalesEtlResult> {
        assertBizMonth(bizdate)
        return request.post<SalesEtlResult>(`${SALES_API}/dws-sales-monthly-region`, undefined, {
            params: { bizdate },
            timeout: SALES_REQUEST_TIMEOUT,
        })
    },

    run(task: SalesTaskKey, dates: SalesTaskDates): Promise<SalesEtlResult | null> {
        switch (task) {
            case 'seed':
                return this.createSeedData()
            case 'ods':
                return this.runOdsSales(dates.dailyBizDate)
            case 'dwd':
                return this.runDwdSalesDetail(dates.dailyBizDate)
            case 'daily':
                return this.runDailySales(dates.dailyBizDate)
            case 'daily-category':
                return this.runDailyCategorySales(dates.dailyBizDate)
            case 'monthly-region':
                return this.runMonthlyRegionSales(dates.monthlyBizDate)
        }
    },
}
