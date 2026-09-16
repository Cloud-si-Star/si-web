import { createApp } from 'vue'
import { createPinia } from 'pinia'
// 引入全局样式
import "./style/main.scss"

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
