<template>
  <div class="layout-wrap">
    <!-- 左侧菜单栏 -->
    <digitalMenu class="menu-con"></digitalMenu>

    <!-- 右侧：子页面渲染位置！！子路由全部渲染在这里 -->
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import digitalMenu from './digital-menu.vue';
</script>

<style scoped lang="scss">
.layout-wrap {
  display: flex;
  height: 100%;
  box-sizing: border-box;
  .menu-con{
    width: 160px;
    height: 100%;
    border: 1px solid #EEE;
  }
}

.main-content {
  flex: 1;
  background: #DDD;
  overflow: hidden;
  box-sizing: border-box;
  padding: 10px;
}
</style>