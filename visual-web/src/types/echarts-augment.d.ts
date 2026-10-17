import 'echarts' // 关键：让文件成为模块，否则会覆盖而非扩充

declare module 'echarts' {
    interface ECElementEvent {
        // 把运行时确实存在、但官方类型没声明的字段补上
        data?: {
            adcode?: number
            name?: string
            value?: number
        }
    }
}