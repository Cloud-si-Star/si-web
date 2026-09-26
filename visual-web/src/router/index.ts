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
    redirect: '/v-digital/d-chat',
    children: [
      {
        path: 'd-table',
        name: 'd-table',
        component: () => import('@/views/d-table/index.vue')
      },
      {
        path: 'd-chat',
        name: 'd-chat',
        component: () => import('@/views/d-chat/index.vue')
      },
      {
        path: 'd-drag',
        name: 'd-drag',
        component: () => import('@/views/d-drag/index.vue')
      },
      {
        path: 'd-demo',
        name: 'd-demo',
        component: () => import('@/views/d-demo/index.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/v-digital'
  }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router;
