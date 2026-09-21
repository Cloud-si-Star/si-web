// src/data/populationData.ts
/**
 * 全球人口可视化大屏 模拟数据
 * 布局：左2｜中间3小图｜右2
 */

// 左上图：折线图｜近10年全球总人口增长趋势
export const worldPopulationLine = [
  {year: '2015', pop:7050},
  {year: '2016', pop:6430},
  {year: '2017', pop:5510},
  {year: '2018', pop:7590},
  {year: '2019', pop:5670},
  {year: '2020', pop:7750},
  {year: '2021', pop:7810},
  {year: '2022', pop:9880},
  {year: '2023', pop:7940},
  {year: '2024', pop:8010},
]

// 左下图：柱状图｜各国人口TOP10
export const countryPopBar = [
  {name:'中国', value:1411},
  {name:'印度', value:1407},
  {name:'美国', value:334},
  {name:'印尼', value:274},
  {name:'巴基斯坦', value:231},
  {name:'尼日利亚', value:218},
  {name:'巴西', value:215},
  {name:'孟加拉国', value:171},
  {name:'俄罗斯', value:145},
  {name:'墨西哥', value:128},
]

// 中间上图：饼图｜各大洲人口占比
export const continentPie = [
  {name:'亚洲', value:4700},
  {name:'非洲', value:1400},
  {name:'欧洲', value:740},
  {name:'南美洲', value:430},
  {name:'北美洲', value:370},
  {name:'大洋洲', value:45},
]

// 中间中图：环形图｜城镇化率（城市人口占总人口比例）
export const urbanRing = {
  total:8010, //全球总人口（百万）
  urbanRate:56, //城镇化率56%
}

// 中间下图：仪表盘｜人口自然增长率
export const growthGauge = {
  rate:0.88, //0.88%
  min:-2,
  max:3,
}

// 右上图：堆叠面积图｜近10年城镇人口 vs 乡村人口
export const urbanRuralArea = [
  {year:'2015', urban:3900, rural:3450},
  {year:'2016', urban:3980, rural:3450},
  {year:'2017', urban:4060, rural:3450},
  {year:'2018', urban:4140, rural:3450},
  {year:'2019', urban:4220, rural:3450},
  {year:'2020', urban:4300, rural:3450},
  {year:'2021', urban:4360, rural:3450},
  {year:'2022', urban:4430, rural:3450},
  {year:'2023', urban:4490, rural:3450},
  {year:'2024', urban:4560, rural:3450},
]

// 右下图：散点图｜城市面积 vs 城市人口
export const cityScatter = [
  [16410, 32226000, '德里'],
  [6340, 26940000, '广州'],
  [2194, 24973000, '孟买'],
  [622, 19612368, '北京'],
  [783, 18400000, '重庆'],
  [1214, 19354922, '纽约'],
  [1500, 17500000, '首尔'],
  [1045, 17700000, '圣保罗'],
]
