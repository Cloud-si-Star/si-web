<template>
  <div class="layout-wrap">
    <div class="fixed-open">
        <el-button
            type="primary"
            @click="handleMenu"
        >
            <Transition mode="out-in">
                <el-icon v-if="isOpen" key="expand">
                    <Expand />
                </el-icon>
                <el-icon v-else key="fold">
                    <Fold />
                </el-icon>
            </Transition>
        </el-button>
    </div>
    <!-- 左侧菜单栏 -->
    <visualMenu :isOpen="isOpen"></visualMenu>

    <!-- 右侧：子页面渲染位置！！子路由全部渲染在这里 -->
    <main class="main-content">
         <Transition mode="out-in">
            <router-view />
         </Transition>
      
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import visualMenu from './visual-menu.vue'
import {ref} from 'vue'

const isOpen = ref<boolean>(false)

const handleMenu= ()=>{
    isOpen.value=!isOpen.value
}  

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

.fixed-open{
    position: fixed;
    
    top: 5px;
    left: 5px;
   
    z-index: 999;
    .el-button {
        color: #60f1e7;
        font-size: 30px;
    }
    .el-button--primary{
        width: 80px;
        height: 40px;
        background-color: rgba(69, 69, 246,0.3);
        border: 1px solid rgba(69, 69, 246,0.3);
        &:hover{
            background-color: rgba(69, 69, 246,0.4);
            border: 1px solid rgba(23, 23, 255, 0.4);
        }
    }

}
</style>