<template>
    <div class="con-page">
        <div>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="模型名称">
                    <el-input v-model="formInline.ai_name" />
                </el-form-item>

                <el-form-item label="模型状态">
                    <el-select v-model="formInline.ai_status" placeholder="Select" style="width: 240px">
                        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>

                <el-form-item label="日期">
                    <el-date-picker v-model="formInline.use_date" type="daterange" single-panel />
                </el-form-item>

            </el-form>
        </div>
        <div class="btn-position">
            <el-button type="primary" @click="queryToService">查 询</el-button>
            <el-button>重 置</el-button>
            <el-button type="success">新 增</el-button>
        </div>
        <div class="table-position">
            <el-table :data="tableData" style="height: 100%;" border>
                <el-table-column label="序号" type="index" width="150" align="center"></el-table-column>
                <el-table-column label="模型ID" prop="ai_id" width="150"></el-table-column>
                <el-table-column label="模型名称" prop="ai_name" width="150"></el-table-column>
                <el-table-column label="模型状态" prop="ai_status" width="150" align="center">
                    <template #default="scope">
                        <el-tag :type="scope.row.ai_status_code == 1 ? 'success' : 'info'" effect="dark">
                            {{ scope.row.ai_status_code === 1 ? '在线' : '离线' }}
                        </el-tag>
                    </template>

                </el-table-column>
                <el-table-column label="调用人数" prop="ai_use" width="150"></el-table-column>
                <el-table-column label="创建时间" prop="create_time" width="240"></el-table-column>
                <el-table-column label="备注" prop="remark" width="300"></el-table-column>
                <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                        <el-button link>编 辑</el-button>
                    </template>
                </el-table-column>


            </el-table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { tableApi, type tableListParams, type tableDTO } from '@/api/table';

const options = [
    {
        label: '全部',
        value: '0'
    },
    {
        label: '在线',
        value: '1'
    },
    {
        label: '离线',
        value: '2'
    }
]

const formInline = ref<tableListParams>({
    ai_name: '',
    ai_status: '',
    use_date: '',
    page: 1,
    pageSize: 10
})

const tableData = ref<tableDTO[]>([])

const queryToService = () => {
    let params: tableListParams = formInline.value
    tableApi.getList(params).then(res => {

        tableData.value = res.list

    }).catch(error => {
        console.log(error)
    })
}


onMounted(() => {
    queryToService()
})

</script>

<style lang="scss" scoped>
.con-page {
    flex-direction: column;
}
</style>
