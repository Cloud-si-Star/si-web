<template>
    <div class="con-page alont-set">
        <section class="filter-bar">
            <el-form :inline="true" :model="filters" @submit.prevent="applyFilters">
                <el-form-item label="菜单名称">
                    <el-input v-model="filters.label" clearable placeholder="按名称搜索" @keyup.enter="applyFilters" />
                </el-form-item>
                <el-form-item label="菜单类型">
                    <el-select v-model="filters.menuType" clearable placeholder="全部类型" class="type-filter">
                        <el-option label="工作台" :value="1" />
                        <el-option label="可视化" :value="2" />
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="filters.visible" clearable placeholder="全部状态" class="status-filter">
                        <el-option label="已启用" :value="1" />
                        <el-option label="已关闭" :value="0" />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :icon="Search" @click="applyFilters">查询</el-button>
                    <el-button :icon="RefreshLeft" @click="resetFilters">重置</el-button>
                </el-form-item>
            </el-form>
        </section>

        <section style="margin:5px 0;">
            <el-button type="primary" :icon="Plus" @click="openCreateDialog">新增菜单</el-button>
        </section>

        <section class="table-section">
            <div class="table-heading">
                <div>
                    <h2>菜单列表</h2>
                    <span>{{ filteredMenuCount }} 项</span>
                </div>
                <el-button text :icon="Refresh" :loading="menuStore.loading" @click="loadMenus">刷新</el-button>
            </div>

            <el-table v-loading="menuStore.loading" :data="visibleTree" row-key="id"
                :tree-props="{ children: 'children' }" default-expand-all border class="menu-table" empty-text="暂无菜单数据">
                <el-table-column prop="label" label="菜单名称" min-width="170" />
                <el-table-column label="类型" width="110">
                    <template #default="{ row }: { row: MenuTreeNode }">
                        <el-tag :type="row.menu_type === 1 ? 'primary' : 'success'" effect="plain">
                            {{ menuTypeLabel(row.menu_type) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="path" label="路由路径" min-width="160" show-overflow-tooltip />
                <el-table-column prop="component" label="组件路径" min-width="180" show-overflow-tooltip />
                <el-table-column prop="icon" label="图标" width="110" show-overflow-tooltip />
                <el-table-column prop="sort_order" label="排序" width="80" align="center" />
                <el-table-column label="状态" width="100" align="center">
                    <template #default="{ row }: { row: MenuTreeNode }">
                        <el-switch :model-value="row.visible === 1" :loading="updatingIds.has(row.id)" inline-prompt
                            active-text="开" inactive-text="关"
                            @change="(enabled: string | number | boolean) => handleVisibilityChange(row, Boolean(enabled))" />
                    </template>
                </el-table-column>
                <el-table-column prop="updated_at" label="更新时间" min-width="165" />
                <el-table-column label="操作" width="100" fixed="right" align="center">
                    <template #default="{ row }: { row: MenuTreeNode }">
                        <el-button link type="danger" :icon="Delete" @click="handleDelete(row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </section>

        <el-dialog v-model="dialogVisible" title="新增菜单" width="560px" destroy-on-close>
            <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px" status-icon>
                <el-form-item label="菜单名称" prop="label">
                    <el-input v-model="form.label" maxlength="50" show-word-limit placeholder="请输入菜单名称" />
                </el-form-item>
                <el-form-item label="父级菜单" prop="parent_id">
                    <el-tree-select v-model="form.parent_id" :data="parentMenuOptions"
                        :props="{ label: 'label', value: 'id', children: 'children' }" check-strictly clearable
                        default-expand-all placeholder="不选则作为顶级菜单" />
                </el-form-item>
                <el-form-item label="菜单类型" prop="menu_type">
                    <el-radio-group v-model="form.menu_type">
                        <el-radio :value="1">工作台</el-radio>
                        <el-radio :value="2">可视化</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="路由路径" prop="path">
                    <el-input v-model="form.path" maxlength="100" placeholder="例如 /system/users" />
                </el-form-item>
                <el-form-item label="组件路径" prop="component">
                    <el-input v-model="form.component" maxlength="100" placeholder="例如 system/user/index" />
                </el-form-item>
                <el-form-item label="菜单图标" prop="icon">
                    <el-input v-model="form.icon" maxlength="50" placeholder="图标名称或图标组件标识" />
                </el-form-item>
                <el-form-item label="排序值" prop="sort_order">
                    <el-input-number v-model="form.sort_order" :min="0" :max="4294967295" controls-position="right" />
                </el-form-item>
                <el-form-item label="初始状态">
                    <el-switch v-model="form.visible" :active-value="1" :inactive-value="0" active-text="启用"
                        inactive-text="关闭" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" :loading="submitting" @click="submitCreate">创建菜单</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Delete, Plus, Refresh, RefreshLeft, Search } from '@element-plus/icons-vue'
import { useMenuStore } from '@/stores/menu'
import { menuApi, type CreateMenuDTO, type MenuTreeNode, type MenuType } from '@/api/menu'

defineOptions({ name: 'MenuManagement' })

interface MenuFilters {
    label: string
    menuType: MenuType | undefined
    visible: 0 | 1 | undefined
}

const submitting = ref(false)
const dialogVisible = ref(false)
const menuStore = useMenuStore()
const appliedFilters = ref<MenuFilters>({ label: '', menuType: undefined, visible: undefined })
const updatingIds = ref(new Set<number>())
const formRef = ref<FormInstance>()
const filters = reactive<MenuFilters>({ label: '', menuType: undefined, visible: undefined })

const createInitialForm = (): CreateMenuDTO => ({
    parent_id: 0,
    label: '',
    icon: '',
    path: '',
    component: '',
    sort_order: 0,
    visible: 1,
    menu_type: 1,
})

const form = reactive<CreateMenuDTO>(createInitialForm())

const formRules: FormRules<CreateMenuDTO> = {
    label: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
    icon: [{ required: true, message: '请输入菜单图标', trigger: 'blur' }],
    path: [{ required: true, message: '请输入路由路径', trigger: 'blur' }],
    component: [{ required: true, message: '请输入组件路径', trigger: 'blur' }],
    menu_type: [{ required: true, message: '请选择菜单类型', trigger: 'change' }],
}

/** 基于后端返回的 children 树筛选，并保留匹配项的父级路径。 */
const visibleTree = computed(() => {
    const query = appliedFilters.value.label.trim().toLocaleLowerCase()
    const filterNodes = (nodes: MenuTreeNode[]): MenuTreeNode[] => nodes.flatMap((node) => {
        const children = node.children ? filterNodes(node.children) : []
        const matches = (!query || node.label.toLocaleLowerCase().includes(query))
            && (appliedFilters.value.menuType === undefined || node.menu_type === appliedFilters.value.menuType)
            && (appliedFilters.value.visible === undefined || node.visible === appliedFilters.value.visible)

        if (!matches && children.length === 0) return []
        return [{ ...node, children: children.length ? children : undefined }]
    })
    return filterNodes(menuStore.menuList)
})

const filteredMenuCount = computed(() => {
    const countNodes = (nodes: MenuTreeNode[]): number => nodes.reduce(
        (count, node) => count + 1 + (node.children ? countNodes(node.children) : 0),
        0,
    )
    return countNodes(visibleTree.value)
})

const parentMenuOptions = computed(() => menuStore.menuList)

const menuTypeLabel = (type: MenuType): string => {
    if (type === 1) return '工作台'
    if (type === 2) return '可视化'
    return '未分类'
}

/** 查询后端菜单树，统一错误处理由 request 拦截器完成。 */
const loadMenus = async (): Promise<void> => {
    try {
        await menuStore.loadMenuTree()
    } catch (error) {
        ElMessage.error(error instanceof Error ? error.message : '菜单列表加载失败')
    }
}

const applyFilters = (): void => {
    appliedFilters.value = { ...filters }
}

const resetFilters = (): void => {
    filters.label = ''
    filters.menuType = undefined
    filters.visible = undefined
    applyFilters()
}

const openCreateDialog = (): void => {
    Object.assign(form, createInitialForm())
    dialogVisible.value = true
}

/** 表单校验通过后新增菜单，并刷新服务端菜单树。 */
const submitCreate = async (): Promise<void> => {
    if (!formRef.value) return
    const valid = await formRef.value.validate().catch(() => false)
    if (!valid) return

    submitting.value = true
    try {
        const payload: CreateMenuDTO = { ...form, parent_id: form.parent_id || 0 }
        await menuApi.create(payload)
        ElMessage.success('菜单创建成功')
        dialogVisible.value = false
        await loadMenus()
    } catch (error) {
        ElMessage.error(error instanceof Error ? error.message : '菜单创建失败')
    } finally {
        submitting.value = false
    }
}

/** 关闭仅更新 visible=0，保留菜单记录；切换失败时刷新服务端状态。 */
const handleVisibilityChange = async (menu: MenuTreeNode, enabled: boolean): Promise<void> => {
    updatingIds.value.add(menu.id)
    try {
        await menuApi.updateVisibility(menu.id, { visible: enabled ? 1 : 0 })
        ElMessage.success(enabled ? '菜单已启用' : '菜单已关闭')
        await loadMenus()
    } catch (error) {
        ElMessage.error(error instanceof Error ? error.message : '菜单状态更新失败')
        await loadMenus()
    } finally {
        updatingIds.value.delete(menu.id)
    }
}

/** 删除为物理删除；确认框提示先处理子菜单约束。 */
const handleDelete = async (menu: MenuTreeNode): Promise<void> => {
    try {
        await ElMessageBox.confirm(
            `确定删除菜单“${menu.label}”吗？如该菜单仍有子菜单，需先删除子菜单。此操作不可恢复。`,
            '删除菜单',
            { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' },
        )
        await menuApi.remove(menu.id)
        ElMessage.success('菜单已删除')
        await loadMenus()
    } catch (error) {
        if (error === 'cancel' || error === 'close') return
        ElMessage.error(error instanceof Error ? error.message : '菜单删除失败')
    }
}

onMounted(loadMenus)
</script>

<style scoped lang="scss">
.alont-set {
    flex-direction: column;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.page-eyebrow {
    margin-bottom: 4px;
    color: #778791;
    font-size: 10px;
    letter-spacing: 1.2px;
}

.page-header h1 {
    font-size: 24px;
    font-weight: 600;
}

.filter-bar,
.table-section {
    padding: 18px 20px;
    background: #fff;
    border: 1px solid #e5eaee;
    border-radius: 6px;
}

.filter-bar {
    padding-bottom: 0;
}

.filter-bar :deep(.el-form-item) {
    margin-bottom: 16px;
}

.filter-bar :deep(.el-input) {
    width: 210px;
}

.type-filter,
.status-filter {
    width: 140px;
}

.table-section {
    flex: 1;
    min-height: 340px;
    display: flex;
    flex-direction: column;
}

.table-heading {
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.table-heading>div {
    display: flex;
    align-items: baseline;
    gap: 10px;
}

.table-heading h2 {
    font-size: 16px;
    font-weight: 600;
}

.table-heading span {
    color: #87949b;
    font-size: 12px;
}

.menu-table {
    width: 100%;
}

@media (max-width: 720px) {
    .menu-page {
        padding: 18px 14px;
        gap: 14px;
    }

    .filter-bar,
    .table-section {
        padding: 14px;
    }

    .filter-bar :deep(.el-input),
    .type-filter,
    .status-filter {
        width: min(100%, 250px);
    }

    .filter-bar :deep(.el-form-item) {
        width: 100%;
        margin-right: 0;
    }
}
</style>