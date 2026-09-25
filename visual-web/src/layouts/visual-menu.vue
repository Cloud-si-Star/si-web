<template>
  <!-- 固定左上角 展开/收起按钮 (value.path+pathLoad)==nowPath -->
  <div class="toggle-btn-wrap" :class="{'toggle-active':isOpen}">
    <div v-for="value in path" @click="pushRoute(value)" class="menu-item" :class="{'active-con':(pathLoad+value.path)==nowPath}">
       <span class="text-span">{{ value.value }}</span>
    </div>
  
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter,useRoute } from 'vue-router'

interface MenuItem{
    path_id:number
    path:string
    name:string
    meta:string
    value:string
}

const route = useRoute()

const nowPath = computed(()=>{
    return route.path
})

const pathLoad = ref<string>('/v-visual')

// 控制侧边栏开关
const props = withDefaults(defineProps<{isOpen:boolean}>(),{
    isOpen:false
})

const path:MenuItem[]=[
    {   
        path_id:10000,
        path:"/v1-view",
        name:"v1-view",
        meta:"数据大屏",
        value:"数据可视化"
    },
    {
        path_id:10001,
        path:"/v2-view",
        name:"v2-view",
        meta:"数据大屏",
        value:"数据并发化"
    },
    {
        path_id:10002,
        path:"/v-digital",
        name:"v-digital",
        meta:"数智管理化",
        value:"数智管理化"
    }
]

const router=useRouter()


function pushRoute(path_route:MenuItem){

    if(path_route.path_id==10002){
        router.push(path_route.path)
        return
    }
    
    let next_path=pathLoad.value+path_route.path

    router.push(next_path)
}


</script>

<style  lang="scss" scoped>
/* 渐变字体 */
// 渐变文字mixin
@mixin gradient-text($startColor, $endColor, $dir: 90deg) {
  background: linear-gradient($dir, $startColor, $endColor);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  // 可选：抗锯齿，大屏文字更平滑
  -webkit-font-smoothing: antialiased;
}
/* 左上角固定按钮，永远悬浮 */
.toggle-btn-wrap {
  position: fixed;
  width: 0px;
  height: 100%;
  top: 0px;
  left: 0px;
  z-index: 99;
  transition: width 2s;
  display: flex;
  align-items: center;
  flex-direction: column;
  padding-top: 60px;
  box-sizing: border-box;
  background: rgba(27, 71, 134);
  color: #FFF;
  overflow: hidden;
  .menu-item{
    border: 1px solid rgba(8, 37, 97,0.5);
    width: 100%;
    text-align: center;
    font-size: 18px;
    height: 40px;
    line-height: 40px;
    margin-bottom: 5px;
    text-wrap: nowrap;
    background: rgba(8, 37, 97,0.5);
    box-sizing: border-box;
    
    &:hover{
        background: linear-gradient(to right,rgba(40, 224, 208, 0.4),rgba(237, 175, 218, 0.8));
        cursor: pointer;
        .text-span{
            @include gradient-text(#4fc3ff, #28e0d0, 90deg);
            font-weight: bold;
        }
        
    }
  }

}

.toggle-active{
    width: 160px;
}

.active-con{
    background: linear-gradient(to right,rgba(40, 224, 208, 0.4),rgba(237, 175, 218, 0.8)) !important;
    cursor: pointer;
    .text-span{
        @include gradient-text(#4fc3ff, #28e0d0, 90deg);
        font-weight: bold !important;
    }
}
</style>