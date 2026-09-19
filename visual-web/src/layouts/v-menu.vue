<template>
  <!-- 固定左上角 展开/收起按钮 -->
  <div>
    <div class="toggle-btn-wrap">
        <el-button
        type="primary"
        circle
        @click="addItem"
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

    <!-- 悬浮侧边栏，带动画 -->
    <div class="side-menu" :class="{ 'menu-close': isOpen }">
        <el-menu
            default-active="$route.path"
            class="el-menu-vertical-demo"
            background-color="#ffffff"
            text-color="#303133"
            active-text-color="#409eff"
            @select="handleSelect"
        >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/chart">图表页面</el-menu-item>
        <el-menu-item index="/user">用户管理</el-menu-item>
        <el-menu-item index="/setting">系统设置</el-menu-item>
        </el-menu>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { userBookStore } from '@/stores/book';
// 控制侧边栏开关
const isOpen = ref(true)


const bookStore=userBookStore()

const addItem = ()=>{
    isOpen.value=!isOpen.value
    let dict_book={
        book_id:1001,
        book_price:120,
        book_name:'实战教程',
        num:1
    }
    bookStore.addBook(dict_book)
}



const handleSelect=(key:string,keyPath:[])=>{
    console.log(bookStore.bookList);
    
}

</script>

<style scoped>
/* 左上角固定按钮，永远悬浮 */
.toggle-btn-wrap {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 999;
}

/* 侧边容器：悬浮定位，不挤压主页面 */
.side-menu {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 220px;
  z-index: 998;
  /* 动画核心 */
  transition: transform 0.35s ease-in-out;
}
/* 关闭状态，向左滑出屏幕 */
.menu-close {
  transform: translateX(-100%);
}

/* 菜单高度撑满 */
:deep(.el-menu-vertical-demo) {
  height: 100%;
  border-right: 1px solid #e4e7ed;
}
</style>