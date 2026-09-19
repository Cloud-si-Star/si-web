<template>
  <div class="layout-wrap">
    <!-- 左侧菜单栏 -->
    <vMenu class="sidebar"></vMenu>

    <!-- 右侧：子页面渲染位置！！子路由全部渲染在这里 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import vMenu from './v-menu.vue'

interface MenuItem{
    path_id:number
    path:string
    name:string
    meta:string
    value:string
}

const path:MenuItem[]=[
    {   
        path_id:10000,
        path:"/v-visual",
        name:"v-visual",
        meta:"数据大屏",
        value:"数据可视化"
    },
    {
        path_id:10001,
        path:"/v-scroll",
        name:"v-scroll",
        meta:"数据大屏",
        value:"数据并发化"
    },
]

const route=useRouter()

function pushRoute(path_route:string){
    route.push(path_route)
}

</script>

<style scoped lang="scss">
.layout-wrap {
  display: flex;
  height: 100%;
  box-sizing: border-box;
}

.main-content {
  flex: 1;
  background: #f5f7fa;
  overflow: auto;
  box-sizing: border-box;
}
</style>
