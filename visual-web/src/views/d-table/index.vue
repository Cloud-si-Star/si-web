<template>


    <main class="ranking-page">

        <section class="summary-grid" aria-label="榜单概览">
            <div class="page-header summary-item">
                <div>
                    <p class="eyebrow">MODEL USAGE WORKSPACE</p>
                    <h1>AI 使用榜单</h1>
                    <p class="page-description">整理模型展示顺序，快速查看使用表现。</p>
                </div>
            </div>
            <div class="summary-item">
                <span>模型数量</span>
                <strong>{{ filteredItems.length }}</strong>
                <small>当前筛选结果</small>
            </div>
            <div class="summary-item">
                <span>总调用量</span>
                <strong>{{ formatNumber(totalUsage) }}</strong>
                <small>所选模型累计</small>
            </div>
            <div class="summary-item">
                <span>领跑模型</span>
                <strong class="leader-name">{{ topModel?.ai_name ?? '暂无' }}</strong>
                <small>{{ topModel ? `${formatNumber(topModel.ai_use)} 次调用` : '没有匹配的模型' }}</small>
            </div>
            <div class="summary-item">
                <el-button :icon="RefreshLeft" @click="restoreDefaultOrder">恢复默认顺序</el-button>
            </div>
        </section>

        <section class="ranking-section">
            <div class="toolbar">
                <el-input v-model="searchText" class="search-input" clearable :prefix-icon="Search"
                    placeholder="搜索模型名称或 ID" aria-label="搜索模型名称或 ID" />
                <div class="toolbar-actions">
                    <span class="sort-label">排序方式</span>
                    <el-radio-group v-model="sortMode" size="default" aria-label="排序方式">
                        <el-radio-button value="manual">手动</el-radio-button>
                        <el-radio-button value="usage">调用量</el-radio-button>
                        <el-radio-button value="name">名称</el-radio-button>
                    </el-radio-group>
                </div>
            </div>

            <div class="list-heading">
                <div>
                    <h2>模型排名</h2>
                    <span>{{ sortMode === 'manual' ? '拖动把手调整顺序' : '当前按规则自动排列' }}</span>
                </div>
                <span class="list-count">{{ filteredItems.length }} 个模型</span>
            </div>

            <div class="ranking-list" role="list" aria-label="可排序的 AI 模型榜单" @dragover.prevent @drop="finishDrag">
                <article v-for="(item, index) in filteredItems" :key="item.ai_id" class="ranking-row" :class="{
                    'is-draggable': sortMode === 'manual',
                    'is-dragging': draggedId === item.ai_id,
                    'is-drop-target': dropTargetId === item.ai_id,
                }" role="listitem" :draggable="sortMode === 'manual'" @dragstart="startDrag($event, item.ai_id)"
                    @dragenter.prevent="setDropTarget(item.ai_id)" @dragover.prevent
                    @drop.stop.prevent="dropOn(item.ai_id)" @dragend="clearDragState">
                    <span class="rank-index">{{ String(index + 1).padStart(2, '0') }}</span>

                    <button class="drag-handle" type="button" :disabled="sortMode !== 'manual'"
                        :aria-label="`拖动 ${item.ai_name} 调整排名`"
                        :title="sortMode === 'manual' ? '拖动调整顺序' : '切换到手动排序后可拖动'"
                        @keydown.up.prevent="moveItem(item.ai_id, -1)" @keydown.down.prevent="moveItem(item.ai_id, 1)">
                        <el-icon>
                            <Rank />
                        </el-icon>
                    </button>

                    <div class="model-mark" :class="`tone-${index % 5}`" aria-hidden="true">
                        {{ item.ai_name.slice(0, 1) }}
                    </div>

                    <div class="model-info">
                        <div class="model-title-line">
                            <h3>{{ item.ai_name }}</h3>
                            <span class="model-id">ID {{ item.ai_id }}</span>
                        </div>
                        <div class="usage-track" role="progressbar" :aria-label="`${item.ai_name} 相对调用量`"
                            :aria-valuenow="item.ai_use" :aria-valuemin="0" :aria-valuemax="maxUsage">
                            <span :style="{ width: `${usagePercent(item.ai_use)}%` }"></span>
                        </div>
                    </div>

                    <div class="usage-value">
                        <strong>{{ formatNumber(item.ai_use) }}</strong>
                        <span>次调用</span>
                    </div>

                    <div class="row-actions" aria-label="调整模型顺序">
                        <el-button text circle :icon="ArrowUp" :disabled="sortMode !== 'manual' || index === 0"
                            :aria-label="`${item.ai_name} 上移`" @click="moveItem(item.ai_id, -1)" />
                        <el-button text circle :icon="ArrowDown"
                            :disabled="sortMode !== 'manual' || index === filteredItems.length - 1"
                            :aria-label="`${item.ai_name} 下移`" @click="moveItem(item.ai_id, 1)" />
                    </div>
                </article>

                <div v-if="filteredItems.length === 0" class="empty-state">
                    <el-icon>
                        <Search />
                    </el-icon>
                    <p>没有找到匹配的模型</p>
                    <el-button text type="primary" @click="searchText = ''">清除搜索条件</el-button>
                </div>
            </div>

            <footer class="list-footer">
                <span class="status-indicator"></span>
                <span>{{ sortMode === 'manual' ? '手动顺序仅保存在当前页面会话' : '自动排序不修改榜单原始顺序' }}</span>
            </footer>
        </section>
    </main>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ElButton, ElIcon, ElInput, ElRadioButton, ElRadioGroup } from 'element-plus'
import { ArrowDown, ArrowUp, Rank, RefreshLeft, Search } from '@element-plus/icons-vue'
import { storeToRefs } from 'pinia'
import { useAiStore } from '@/stores/ai_item'

defineOptions({ name: 'AiRankingBoard' })

type SortMode = 'manual' | 'usage' | 'name'

const aiStore = useAiStore()
const { aiTable } = storeToRefs(aiStore)

const searchText = ref('')
const sortMode = ref<SortMode>('manual')
const manualOrder = ref<number[]>(aiTable.value.map((item) => item.ai_id))
const draggedId = ref<number | null>(null)
const dropTargetId = ref<number | null>(null)

/** 新增模型時把新 ID 追加到手動順序末尾，刪除模型時清除過期 ID。 */
watch(aiTable, (items) => {
    const currentIds = new Set(items.map((item) => item.ai_id))
    manualOrder.value = manualOrder.value.filter((id) => currentIds.has(id))
    items.forEach((item) => {
        if (!manualOrder.value.includes(item.ai_id)) manualOrder.value.push(item.ai_id)
    })
}, { deep: true })

const filteredItems = computed(() => {
    const query = searchText.value.trim().toLocaleLowerCase()
    const matches = aiTable.value.filter((item) =>
        item.ai_name.toLocaleLowerCase().includes(query) || String(item.ai_id).includes(query),
    )

    if (sortMode.value === 'usage') {
        return [...matches].sort((left, right) => right.ai_use - left.ai_use)
    }
    if (sortMode.value === 'name') {
        return [...matches].sort((left, right) => left.ai_name.localeCompare(right.ai_name, 'zh-CN'))
    }

    const orderIndex = new Map(manualOrder.value.map((id, index) => [id, index]))
    return [...matches].sort((left, right) =>
        (orderIndex.get(left.ai_id) ?? Number.MAX_SAFE_INTEGER)
        - (orderIndex.get(right.ai_id) ?? Number.MAX_SAFE_INTEGER),
    )
})

const totalUsage = computed(() => filteredItems.value.reduce((total, item) => total + item.ai_use, 0))
const topModel = computed(() => [...filteredItems.value].sort((left, right) => right.ai_use - left.ai_use)[0])
const maxUsage = computed(() => Math.max(1, ...filteredItems.value.map((item) => item.ai_use)))

const formatNumber = (value: number): string => new Intl.NumberFormat('zh-CN').format(value)

const usagePercent = (usage: number): number => Math.max(3, Math.round((usage / maxUsage.value) * 100))

/** 将一条记录移到另一条记录所在位置，用于拖拽和按钮键盘替代操作。 */
const reorderItems = (sourceId: number, targetId: number): void => {
    if (sortMode.value !== 'manual' || sourceId === targetId) return

    const nextOrder = [...manualOrder.value]
    const sourceIndex = nextOrder.indexOf(sourceId)
    const targetIndex = nextOrder.indexOf(targetId)
    if (sourceIndex < 0 || targetIndex < 0) return

    nextOrder.splice(sourceIndex, 1)
    nextOrder.splice(targetIndex, 0, sourceId)
    manualOrder.value = nextOrder
}

const moveItem = (itemId: number, offset: -1 | 1): void => {
    if (sortMode.value !== 'manual') return
    const visibleIds = filteredItems.value.map((item) => item.ai_id)
    const visibleIndex = visibleIds.indexOf(itemId)
    const targetId = visibleIds[visibleIndex + offset]
    if (targetId !== undefined) reorderItems(itemId, targetId)
}

const startDrag = (event: DragEvent, itemId: number): void => {
    if (sortMode.value !== 'manual' || !event.dataTransfer) {
        event.preventDefault()
        return
    }
    draggedId.value = itemId
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', String(itemId))
}

const setDropTarget = (itemId: number): void => {
    if (draggedId.value !== null && draggedId.value !== itemId) dropTargetId.value = itemId
}

const dropOn = (targetId: number): void => {
    const sourceId = draggedId.value
    if (sourceId !== null) reorderItems(sourceId, targetId)
    clearDragState()
}

const finishDrag = (event: DragEvent): void => {
    event.preventDefault()
    const sourceId = draggedId.value
    const targetId = dropTargetId.value
    if (sourceId !== null && targetId !== null) reorderItems(sourceId, targetId)
    clearDragState()
}

const clearDragState = (): void => {
    draggedId.value = null
    dropTargetId.value = null
}

const restoreDefaultOrder = (): void => {
    manualOrder.value = aiTable.value.map((item) => item.ai_id)
    sortMode.value = 'manual'
    searchText.value = ''
}
</script>

<style scoped lang="scss">
.ranking-page {
    --ink: #26333a;
    --muted: #77868c;
    --line: #e1e8e9;
    --teal: #147d78;
    --teal-soft: #e7f4f1;
    width: 100%;
    height: 100%;
    min-height: 500px;
    overflow: auto;
    padding: 28px clamp(18px, 3vw, 42px);
    display: flex;
    gap: 22px;
    background: #f3f6f5;
    color: var(--ink);
}





.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
}

.eyebrow {
    margin-bottom: 5px;
    color: var(--teal);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.page-header h1 {
    font-size: 25px;
    font-weight: 650;
}

.page-description {
    margin-top: 4px;
    color: var(--muted);
    font-size: 12px;
}

.page-header :deep(.el-button) {
    min-height: 36px;
    border-color: #cbd8d8;
    color: #405257;
}

.summary-grid {
    // display: grid;
    // grid-template-columns: repeat(3, minmax(0, 1fr));
    display: flex;
    flex-direction: column;
    border-block: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.55);
}

.summary-item {
    min-width: 0;
    padding: 15px 20px;
    display: flex;
    flex-direction: column;
    gap: 3px;
    border-right: 1px solid var(--line);
    background: rgba(255, 255, 255, 1);
    margin-bottom: 15px;
}

.summary-item:last-child {
    border-right: 0;
}

.summary-item>span,
.summary-item small {
    color: var(--muted);
    font-size: 11px;
}

.summary-item strong {
    overflow: hidden;
    color: var(--ink);
    font-size: 23px;
    line-height: 1.25;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
}

.summary-item .leader-name {
    color: var(--teal);
    font-size: 19px;
}

.ranking-section {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
}

.toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--line);
}

.search-input {
    max-width: 340px;
}

.search-input :deep(.el-input__wrapper) {
    min-height: 38px;
    background: #fff;
    box-shadow: 0 0 0 1px #dce5e5 inset;
}

.toolbar-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sort-label {
    color: var(--muted);
    font-size: 11px;
}

.toolbar-actions :deep(.el-radio-button__inner) {
    min-width: 54px;
    padding: 8px 12px;
    border-color: #d8e2e2;
    box-shadow: none;
}

.toolbar-actions :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    border-color: var(--teal);
    background: var(--teal);
    box-shadow: -1px 0 0 0 var(--teal);
}

.list-heading {
    padding: 18px 2px 12px;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
}

.list-heading>div {
    display: flex;
    align-items: baseline;
    gap: 11px;
}

.list-heading h2 {
    font-size: 15px;
    font-weight: 650;
}

.list-heading span,
.list-count {
    color: var(--muted);
    font-size: 11px;
}

.ranking-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.ranking-row {
    min-height: 78px;
    padding: 10px 14px;
    display: grid;
    grid-template-columns: 36px 28px 42px minmax(100px, 1fr) minmax(100px, 150px) 72px;
    align-items: center;
    gap: 12px;
    border: 1px solid #e4eaea;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.88);
    transition: border-color 140ms ease, background-color 140ms ease, opacity 140ms ease;
}

.ranking-row.is-draggable {
    cursor: default;
}

.ranking-row.is-dragging {
    opacity: 0.42;
}

.ranking-row.is-drop-target {
    border-color: #288f89;
    background: #eff9f6;
}

.rank-index {
    color: #839399;
    font-size: 12px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    text-align: center;
}

.drag-handle {
    width: 28px;
    height: 34px;
    display: grid;
    place-items: center;
    border: 0;
    border-radius: 4px;
    background: transparent;
    color: #788a8e;
    cursor: grab;
}

.drag-handle:disabled {
    color: #b6c0c2;
    cursor: not-allowed;
}

.drag-handle:not(:disabled):hover,
.drag-handle:not(:disabled):focus-visible {
    outline: 0;
    background: var(--teal-soft);
    color: var(--teal);
}

.drag-handle:not(:disabled):active {
    cursor: grabbing;
}

.model-mark {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    border-radius: 4px;
    color: #fff;
    font-size: 15px;
    font-weight: 700;
}

.tone-0 {
    background: #1d756f;
}

.tone-1 {
    background: #c0784d;
}

.tone-2 {
    background: #526f91;
}

.tone-3 {
    background: #85824a;
}

.tone-4 {
    background: #7b637e;
}

.model-info {
    min-width: 0;
}

.model-title-line {
    display: flex;
    align-items: baseline;
    gap: 9px;
}

.model-title-line h3 {
    overflow: hidden;
    font-size: 14px;
    font-weight: 600;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.model-id {
    flex: none;
    color: #89989d;
    font-size: 10px;
    font-variant-numeric: tabular-nums;
}

.usage-track {
    height: 4px;
    margin-top: 10px;
    overflow: hidden;
    border-radius: 3px;
    background: #e9eeee;
}

.usage-track span {
    height: 100%;
    display: block;
    border-radius: inherit;
    background: linear-gradient(90deg, #368e85, #8fc8b2);
    transition: width 240ms ease;
}

.usage-value {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 1px;
}

.usage-value strong {
    color: #34464b;
    font-size: 15px;
    font-variant-numeric: tabular-nums;
}

.usage-value span {
    color: #8a989c;
    font-size: 10px;
}

.row-actions {
    display: flex;
    justify-content: flex-end;
}

.row-actions :deep(.el-button) {
    width: 30px;
    height: 30px;
    margin: 0;
    color: #65797e;
}

.row-actions :deep(.el-button:not(.is-disabled):hover) {
    background: var(--teal-soft);
    color: var(--teal);
}

.empty-state {
    min-height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: #8c9a9f;
}

.empty-state>.el-icon {
    font-size: 24px;
}

.empty-state p {
    font-size: 13px;
}

.list-footer {
    margin-top: auto;
    padding: 14px 2px 0;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #849397;
    font-size: 10px;
}

.status-indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6bb49a;
}

@media (max-width: 760px) {
    .ranking-page {
        height: auto;
        min-height: 100%;
        padding: 20px 14px;
        gap: 16px;
    }

    .summary-item {
        padding: 12px 10px;
    }

    .summary-item strong {
        font-size: 18px;
    }

    .toolbar {
        align-items: stretch;
        flex-direction: column;
        gap: 12px;
    }

    .search-input {
        max-width: none;
    }

    .toolbar-actions {
        justify-content: space-between;
    }

    .ranking-row {
        grid-template-columns: 26px 28px 36px minmax(0, 1fr) 82px;
        gap: 8px;
        padding: 9px;
    }

    .model-mark {
        width: 34px;
        height: 34px;
    }

    .usage-value strong {
        font-size: 12px;
    }

    .row-actions {
        grid-column: 4 / -1;
        justify-content: flex-end;
        margin-top: -6px;
    }
}

@media (max-width: 420px) {
    .page-header h1 {
        font-size: 21px;
    }

    .page-header :deep(.el-button) {
        padding: 8px 10px;
        font-size: 11px;
    }

    .summary-item {
        padding-inline: 7px;
    }

    .summary-item>span,
    .summary-item small {
        font-size: 9px;
    }

    .toolbar-actions :deep(.el-radio-button__inner) {
        min-width: 46px;
        padding-inline: 8px;
    }
}
</style>