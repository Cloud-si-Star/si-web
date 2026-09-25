<template>
  <!-- 外层div包裹，控制宽高，菜单继承 -->
  <div class="menu-wrap">
    <!-- 侧边菜单，背景白色 -->
    <el-menu
      :default-active="activeRoute"
      router
      background-color="#ffffff"
      text-color="#333333"
      active-text-color="#1890ff"
      @select="handleMenuSelect"
    >
      <el-menu-item
        v-for="item in menuList"
        :key="item.path"
        :index="item.path"
      >
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

const route = useRoute()
// 当前激活菜单，自动根据路由高亮
const activeRoute = computed(() => route.path)

// 菜单数组，你可以从pinia/接口获取
const menuList = [
  {
    label: 'AI对话',
    path: '/v-digital/d2-view'
  },
  {
    label: '数据仓库',
    path: '/v-digital/d1-view'
  },
  {
    label: '数据管理',
    path: '/search'
  },
  {
    label: '动态组件',
    path: '/drag-page'
  },
  {
    label: '数据大屏',
    path: '/v-visual'
  }
]

// 点击事件
const handleMenuSelect = (key: string) => {
  console.log('点击菜单，跳转路由：', key)
  // 开启 el-menu 的 router 属性后，会自动 $router.push(key)，不用手动写push
}
</script>

<style scoped>
.menu-wrap {
  width: 100%;
  height: 100%;
}
.menu-wrap :deep(.el-menu) {
  width: inherit;
  height: inherit;
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
