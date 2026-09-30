import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { menuApi, type MenuTreeNode } from '@/api/menu'

/** 菜单树共享状态，管理页和侧边菜单均可复用后端返回的数据。 */
export const useMenuStore = defineStore('menu', () => {
    const menuList = ref<MenuTreeNode[]>([])

    const loading = ref(false)

    /** 从后端获取已组装好的菜单树，并统一维护加载状态。 */
    const loadMenuTree = async (): Promise<MenuTreeNode[]> => {
        loading.value = true
        try {
            menuList.value = await menuApi.getList()
            return menuList.value
        } finally {
            loading.value = false
        }
    }

    const workbenchMenuList = computed(() => {
        return menuList.value.filter((menu) => menu.menu_type === 1)
    })

    const visualMenuList = computed(() => {
        return menuList.value.filter((menu) => menu.menu_type === 2)
    })


    return {
        menuList,
        visualMenuList,
        workbenchMenuList,
        loading,
        loadMenuTree,
    }
})