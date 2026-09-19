import type {InjectionKey} from 'vue'
import type * as ECharts from 'echarts'

export const echartsKey:InjectionKey<typeof ECharts> = Symbol('$echarts')