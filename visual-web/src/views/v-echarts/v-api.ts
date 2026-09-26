import { computed, ref, watch } from 'vue'
import { worldPopulationLine, countryPopBar } from '@/utils/mock_v1'
import type { EChartsOption } from 'echarts'
import * as echarts from 'echarts'
import { useAiStore } from '@/stores/ai_item'
import { storeToRefs } from 'pinia'

const user_ai_store = useAiStore()

// ✅ storeToRefs 把 state 转为 ref，保留响应式
const { aiTable } = storeToRefs(user_ai_store)

/* 左下图形option */
const chart_bar_data = computed(() => {
    const x: string[] = []
    const y: number[] = []
    aiTable.value.forEach(i => {
        x.push(i.ai_name)
        y.push(i.ai_use)
    })
    console.log(123);

    return { x, y }
})


/* 左上图形option */
const chart_line_data = computed(() => {
    const x: string[] = []
    const y: number[] = []
    worldPopulationLine.forEach(i => {
        x.push(i.year)
        y.push(i.pop)
    })
    return { x, y }
})

export const vLine_dataOpt = ref<EChartsOption>({
    xAxis: {
        type: 'category',
        data: chart_line_data.value.x,
        axisLabel: {
            color: '#e8e8e8',
        },
        axisLine: {

            lineStyle: {
                color: 'rgba(140, 160, 180, 0.3)'
            }
        },
        splitLine: {
            show: true, // 纵向网格线（x轴分割线）
            lineStyle: {
                type: 'dashed', // 虚线
                color: 'rgba(120,150,180,0.25)', // 浅色，调低透明度
                width: 1
            }
        },
    },
    yAxis: {
        type: 'value',
        splitLine: {
            show: false
        },
        axisLabel: {
            color: '#e8e8e8',
        },
    },
    tooltip: {
        show: true,
        trigger: 'axis',
        backgroundColor: 'rgba(112, 98, 235,0.2)',
        textStyle: {
            color: '#FFF'
        },
        formatter: (params) => {
            const item = Array.isArray(params) ? params[0] : params
            if (!item) return ''
            return `时间：${item.name}年<br/>世界总人口:${item.value}(千万)`
        }
    },
    series: [
        {
            type: 'line',
            data: chart_line_data.value.y,
            smooth: true,
            // ========== 折线线条渐变色【清亮色】==========
            lineStyle: {
                width: 3,
                color: {
                    type: 'linear',
                    x: 1,
                    y: 0,
                    x2: 0,
                    y2: 0,
                    colorStops: [
                        { offset: 0, color: '#40e0d0' },
                        { offset: 1, color: '#36c9ff' }
                    ]
                }
            },
            // ========== 从上到下光影渐变填充 areaStyle（你说的光影）==========
            areaStyle: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [
                        { offset: 0, color: 'rgba(64, 224, 208, 0.35)' },
                        { offset: 1, color: 'rgba(64, 224, 208, 0.01)' }
                    ]
                }
            },
            itemStyle: {
                // 圆点填充色
                color: '#40e0d0'
            },
        }
    ]
})


/* 右上图形option */

/* 右下图形option */


/* 中1图形option */

export const middleoption = ref<EChartsOption>({
    series: [
        {
            type: 'gauge',
            axisLine: {

                lineStyle: {
                    width: 20,

                    color: [
                        [0.3, '#67e0e3'],
                        [0.7, '#37a2da'],
                        [1, '#edafda']
                    ]
                }
            },
            radius: '95%',
            pointer: {
                itemStyle: {
                    color: 'auto'
                }
            },
            axisTick: {
                distance: -20,
                length: 6,
                lineStyle: {
                    color: '#fff',
                    width: 2
                }
            },
            splitLine: {
                distance: -20,
                length: 20,
                lineStyle: {
                    color: '#fff',
                    width: 4
                }
            },
            axisLabel: {
                color: 'inherit',
                distance: 20,
                fontSize: 14
            },
            detail: {
                valueAnimation: true,
                formatter: '{value} km/h',
                color: 'inherit'
            },
            data: [
                {
                    value: 60,
                    detail: {
                        fontSize: 16
                    }
                }
            ]
        }
    ]
})

/* 中2图形option */
export const middle_3_option = ref<EChartsOption>({
    tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(112, 98, 235,0.15)',
        textStyle: {
            color: '#FFF'
        }
    },
    legend: {
        top: 'center',
        left: '2%',
        orient: 'vertical',
        textStyle: {
            color: '#FFF'
        }
    },
    series: [
        {
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
                borderRadius: 10
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: false,
                    fontSize: 40,
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            color: [
                "#516b91",
                "#59c4e6",
                "#edafda",
                "#93b7e3",
                "#a5e7f0",
                "#cbb0e3"
            ],
            data: [
                { value: 1048, name: 'Search Engine' },
                { value: 735, name: 'Direct' },
                { value: 580, name: 'Email' },
                { value: 484, name: 'Union Ads' },
                { value: 300, name: 'Video Ads' }
            ]
        }
    ]
})

export const middle_2_option = ref<EChartsOption>({
    xAxis: {
        splitLine: {
            show: true, // 纵向网格线（x轴分割线）
            lineStyle: {
                type: 'dashed', // 虚线
                color: 'rgba(120,150,180,0.25)', // 浅色，调低透明度
                width: 1
            }
        },
        axisLine: {
            lineStyle: {
                color: '#EEE'
            }
        },
        axisLabel: {
            color: '#EEE'
        }
    },
    yAxis: {
        splitLine: {
            show: true, // 纵向网格线（x轴分割线）
            lineStyle: {
                type: 'dashed', // 虚线
                color: 'rgba(120,150,180,0.25)', // 浅色，调低透明度
                width: 1
            }
        },
        axisLine: {
            lineStyle: {
                color: '#EEE'
            }
        },
        axisLabel: {
            color: '#EEE'
        }
    },
    grid: {
        top: '9%',
        bottom: '9%',
        left: '9%',
        width: '100%',
        height: '100%'
    },
    series: [
        {
            symbolSize: 20,
            color: [
                "#516b91",
                "#59c4e6",
                "#edafda",
                "#93b7e3",
                "#a5e7f0",
                "#cbb0e3"
            ],
            colorBy: 'data',
            data: [
                [10.0, 8.04],
                [8.07, 6.95],
                [13.0, 7.58],
                [9.05, 8.81],
                [11.0, 8.33],
                [14.0, 7.66],
                [13.4, 6.81],
                [10.0, 6.33],
                [14.0, 8.96],
                [12.5, 6.82],
                [9.15, 7.2],
                [11.5, 7.2],
                [3.03, 4.23],
                [12.2, 7.83],
                [2.02, 4.47],
                [1.05, 3.33],
                [4.05, 4.96],
                [6.03, 7.24],
                [12.0, 6.26],
                [12.0, 8.84],
                [7.08, 5.82],
                [5.02, 5.68]
            ],
            type: 'scatter'
        }
    ]
})