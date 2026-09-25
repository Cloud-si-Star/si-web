import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Layout from "@/layouts/index.vue"


const route: Array<RouteRecordRaw> = [
    {
        path: "/",
        component: Layout,
        redirect: "/v-visual",
        children: [
            {
                path: "/v-visual",
                name: "v-visual",
                component: () => import("@/view/v-echarts/view-visual.vue")
            },
            {
                path: "/v-scroll",
                name: "v-scroll",
                component: () => import("@/view/v-scorll/view-scroll.vue")
            }
        ]
    }
]


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: route,
})

export default router
