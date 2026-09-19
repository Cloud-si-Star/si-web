import { createApp } from 'vue'
import { createPinia } from 'pinia'
// 引入全局样式
import "./style/main.scss"

import App from './App.vue'
import router from './router'

import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css";
// ===== 全局组件 =====
import * as ElementPlusIcons from "@element-plus/icons-vue";
import * as echarts from 'echarts'
import { echartsKey } from '@/types/keys.ts'


const app = createApp(App)
// 2️⃣ 全局组件（Element Plus 图标）
Object.entries(ElementPlusIcons).forEach(([name, comp]) => app.component(name, comp));



app.use(createPinia())
app.use(router)

// 全局注入
app.provide(echartsKey,echarts)


app.mount('#app')
