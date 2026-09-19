import { createApp } from 'vue'
import { createPinia } from 'pinia'
// 引入全局样式
import "./style/main.scss"

import App from './App.vue'
import router from './router'

// Element-plus引入
// 重点：样式必须先引入
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// echarts 主题引入
import westerosTheme from  '@/utils/westeros.ts'

// ===== 全局组件 =====
import * as ElementPlusIcons from "@element-plus/icons-vue";
import * as echarts from 'echarts'
import { echartsKey } from '@/types/keys.ts'
echarts.registerTheme('westeros',westerosTheme)

const app = createApp(App)
// 2️⃣ 全局组件（Element Plus 图标）
Object.entries(ElementPlusIcons).forEach(([name, comp]) => app.component(name, comp));

app.use(ElementPlus, { locale: zhCn })


app.use(createPinia())
app.use(router)

// 全局注入
app.provide(echartsKey,echarts)


app.mount('#app')
