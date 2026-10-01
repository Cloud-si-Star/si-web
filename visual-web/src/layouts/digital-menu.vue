<template>
  <!-- 外层div包裹，控制宽高，菜单继承 -->
  <div class="menu-wrap">
    <div class="logo-box" @click="$router.push('/v-visual')">
      <vlogo></vlogo>
      <span>数智工作台</span>
    </div>
    <!-- 侧边菜单，背景白色 -->
    <el-menu :default-active="activeRoute" router background-color="#ffffff" text-color="#333333"
      active-text-color="#1890ff" @select="handleMenuSelect">
      <el-menu-item v-for="item in menu" :key="item.path" :index="item.path">
        <template #title>
          {{ item.label }}
        </template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMenuStore } from '@/stores/menu.ts'
import vlogo from '@/components/v-logo.vue'

const route = useRoute()
// 当前激活菜单，自动根据路由高亮
const activeRoute = computed(() => route.path)

const menu = useMenuStore().workbenchMenuList

// 点击事件
const handleMenuSelect = (key: string) => {
  console.log('点击菜单，跳转路由：', key)
  // 开启 el-menu 的 router 属性后，会自动 $router.push(key)，不用手动写push
}
</script>

<style scoped>
.logo-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  cursor: pointer;
  height: 45px;
}

.menu-wrap {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.menu-wrap :deep(.el-menu) {
  width: inherit;
  height: calc(100% - 45px);
  border-right: none;
}

/* 自定义hover样式，覆盖element默认 */
:deep(.el-menu-item:hover) {
  background-color: #f0f7ff !important;
}

:deep(.el-menu-item.is-active) {
  background-color: #e6f1ff !important;
}
</style>
