<template>
    <div class="con-page single-page">
        <!-- 操作工具栏 -->
        <div class="toolbar">
            <button @click="addNode">添加节点</button>
            <button @click="exportData">导出数据</button>
            <button @click="importData">导入示例数据</button>
            <button @click="clearCanvas">清空画布</button>
            <span class="tip">拖动节点可看到对齐线 | 空白处拖拽可框选</span>
        </div>
        <!-- X6 画布容器 -->
        <div ref="containerRef" class="x6-container"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Graph, Snapline, Selection } from '@antv/x6'

// ==================== 类型定义 ====================
/** 节点数据结构，用于导出/导入 */
interface GraphData {
    nodes: Array<{
        id: string
        x: number
        y: number
        width: number
        height: number
        label: string
        shape?: string
        attrs?: Record<string, any>
    }>
    edges: Array<{
        id?: string
        source: string
        target: string
        label?: string
    }>
}

// ==================== 响应式引用 ====================
const containerRef = ref<HTMLElement | null>(null)
let graph: Graph | null = null
let nodeIndex = 0  // 用于生成递增的节点 id

// ==================== 初始化画布 ====================
onMounted(() => {
    if (!containerRef.value) return

    // 1. 创建 Graph 实例 [citation:2]
    graph = new Graph({
        container: containerRef.value,
        // width: 800,
        // height: 600,
        autoResize: true,
        background: {
            color: '#F2F7FA',
        },
        grid: {
            size: 10,
            visible: true,
        },
    })

    // 2. 启用对齐线插件 (Snapline) [citation:4][citation:14]
    // 拖动节点时，与其它节点边缘/中心对齐会自动显示参考线
    graph.use(
        new Snapline({
            enabled: true,
            tolerance: 10,    // 对齐精度 10px
            sharp: false,     // 显示贯穿画布的长线
            clean: true,      // 自动清理对齐线 DOM
        }),
    )

    // 3. 启用框选插件 (Selection) [citation:3][citation:8]
    // 支持点击选中 + 空白处拖拽框选，按住 Ctrl/Cmd 可多选
    graph.use(
        new Selection({
            enabled: true,
            multiple: true,           // 启用点击多选
            rubberband: true,         // 启用框选
            movable: true,            // 拖动选框时同时移动选中节点
            strict: false,            // 选框与节点相交即可选中
            modifiers: 'alt',         // 按住 alt 键拖拽才是框选（避免与画布平移冲突）
            showNodeSelectionBox: true, // 显示节点选中框
        }),
    )

    // 4. 绘制初始示例节点和边
    const node1 = graph.addNode({
        id: 'node-1',
        x: 100,
        y: 100,
        width: 100,
        height: 40,
        label: '开始',
        attrs: {
            body: {
                stroke: '#8f8f8f',
                strokeWidth: 1,
                fill: '#fff',
                rx: 6,
                ry: 6,
            },
            label: {
                fill: '#333',
                fontSize: 14,
            },
        },
    })

    const node2 = graph.addNode({
        id: 'node-2',
        x: 350,
        y: 250,
        width: 100,
        height: 40,
        label: '结束',
        attrs: {
            body: {
                stroke: '#8f8f8f',
                strokeWidth: 1,
                fill: '#fff',
                rx: 6,
                ry: 6,
            },
            label: {
                fill: '#333',
                fontSize: 14,
            },
        },
    })

    graph.addEdge({
        source: node1,
        target: node2,
        label: '流程',
        attrs: {
            line: {
                stroke: '#5F95FF',
                strokeWidth: 2,
                targetMarker: {
                    name: 'classic',
                    size: 8,
                },
            },
        },
    })

    // 居中显示所有内容
    graph.centerContent()
})

// ==================== 工具方法 ====================

/** 添加一个新节点到画布 */
function addNode() {
    if (!graph) return
    nodeIndex++
    const id = `node-${Date.now()}`

    graph.addNode({
        id,
        x: 100 + (nodeIndex % 5) * 120,
        y: 50 + Math.floor(nodeIndex / 5) * 80,
        width: 100,
        height: 40,
        label: `节点 ${nodeIndex}`,
        attrs: {
            body: {
                stroke: '#8f8f8f',
                strokeWidth: 1,
                fill: '#fff',
                rx: 6,
                ry: 6,
            },
            label: {
                fill: '#333',
                fontSize: 14,
            },
        },
    })
}

/** 导出画布数据为 JSON [citation:5][citation:15] */
function exportData() {
    if (!graph) return
    const data = graph.toJSON()
    console.log('导出的画布数据:', JSON.stringify(data, null, 2))

    // 模拟保存到后端：这里仅打印到控制台
    // 实际使用时可以发送到服务器：
    // await fetch('/api/save-graph', { method: 'POST', body: JSON.stringify(data) })
    alert('画布数据已导出到控制台，请按 F12 查看')
}

/** 导入示例数据（模拟从后端加载） [citation:5] */
function importData() {
    if (!graph) return

    const sampleData: GraphData = {
        nodes: [
            {
                id: 'import-node-1',
                x: 200,
                y: 100,
                width: 100,
                height: 40,
                label: '导入节点A',
                shape: 'rect',
            },
            {
                id: 'import-node-2',
                x: 450,
                y: 200,
                width: 100,
                height: 40,
                label: '导入节点B',
                shape: 'rect',
            },
        ],
        edges: [
            {
                id: 'import-edge-1',
                source: 'import-node-1',
                target: 'import-node-2',
                label: '连接',
            },
        ],
    }

    // 清空画布后导入
    graph.clearCells()
    graph.fromJSON(sampleData)
    graph.centerContent()
}

/** 清空画布 */
function clearCanvas() {
    if (!graph) return
    graph.clearCells()
}

// ==================== 清理 ====================
onUnmounted(() => {
    graph?.dispose()
    graph = null
})
</script>

<style scoped>
.single-page {
    flex-direction: column;
}

.toolbar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: #f5f5f5;
    border-radius: 6px 6px 0 0;
    border: 1px solid #e0e0e0;
    border-bottom: none;
}

.toolbar button {
    padding: 6px 14px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    background: #fff;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
}

.toolbar button:hover {
    border-color: #5F95FF;
    color: #5F95FF;
}

.toolbar .tip {
    margin-left: auto;
    font-size: 12px;
    color: #999;
}

.x6-container {
    width: 100%;
    /* height: 600px; */
    border: 1px solid #e0e0e0;
    border-radius: 0 0 6px 6px;
    background: #fff;
}
</style>