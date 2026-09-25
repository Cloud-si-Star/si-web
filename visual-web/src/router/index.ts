import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"

const LayoutVisual = () => import('@/layouts/layout-visual.vue')

const LayoutDigital = () => import('@/layouts/layout-digital.vue')

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/v-visual'
  },
  {
    name: 'visual',
    path: '/v-visual',
    redirect: '/v-visual/v1-view',
    component: LayoutVisual,
    children: [
      {
        path: 'v1-view',
        name: 'v1-view',
        component: () => import('@/views/v-echarts/view-visual.vue')
      },
      {
        path: 'v2-view',
        name: 'v2-view',
        component: () => import('@/views/v-scorll/view-scroll.vue')
      }
    ]
  },
  {
    name: 'digital',
    path: '/v-digital',
    component: LayoutDigital,
    redirect: '/v-digital/d1-view',
    children: [
      {
        path: 'd1-view',
        name: 'd1-view',
        component: () => import('@/views/d-table/index.vue')
      },
      {
        path: 'd2-view',
        name: 'd2-view',
        component: () => import('@/views/d-chat/index.vue')
      }
    ]
  }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router;