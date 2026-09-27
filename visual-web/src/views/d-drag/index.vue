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
            <el-button type="primary" @click="debouncedSearch">查 询</el-button>
            <el-button @click="resetForm">重 置</el-button>
            <el-button type="success">新 增</el-button>
        </div>
        <div class="table-position">
            <el-table :data="tableData" style="height: 100%;" border>
                <el-table-column label="序号" type="index" width="150" align="center"></el-table-column>
                <el-table-column label="模型ID" prop="ai_id" width="150"></el-table-column>
                <el-table-column label="模型名称" prop="ai_name" width="150"></el-table-column>
                <el-table-column label="模型状态" prop="ai_status" width="150" align="center">
                    <template #default="scope">
                        <el-tag :type="scope.row.ai_status == '1' ? 'success' : 'info'" effect="dark">
                            {{ scope.row.ai_status == '1' ? '在线' : '离线' }}
                        </el-tag>
                    </template>

                </el-table-column>
                <el-table-column label="调用人数" prop="ai_use" width="150"></el-table-column>
                <el-table-column label="创建时间" prop="create_time" width="240"></el-table-column>
                <el-table-column label="备注" prop="remark" width="300"></el-table-column>
                <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                        <el-button link type="primary" @click="edit(scope.row)">编 辑</el-button>
                    </template>
                </el-table-column>


            </el-table>
        </div>
        <el-dialog v-model="dialogFormVisible" title="编辑模型" width="500">
            <el-form :model="dialogForm" ref="ruleFormRef" :rules="rules">
                <el-form-item label="模型ID" prop="ai_name">
                    <el-input v-model="dialogForm.ai_id" autocomplete="off" disabled />
                </el-form-item>
                <el-form-item label="模型名称" prop="ai_name">
                    <el-input v-model="dialogForm.ai_name" autocomplete="off" />
                </el-form-item>
                <el-form-item label="模型状态" prop="ai_status">
                    <el-select v-model="dialogForm.ai_status" placeholder="Please select a status">
                        <el-option label="在线" value="1" />
                        <el-option label="离线" value="0" />
                    </el-select>
                </el-form-item>
                <el-form-item label="模型描述" prop="remark">
                    <el-input type="textarea" v-model="dialogForm.remark" autocomplete="off" />
                </el-form-item>

            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="submit(ruleFormRef)">
                        提交
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { tableApi, type tableListParams, type tableDTO, type UpdateTableDTO } from '@/api/table';
import { debounce, throttle } from '@/utils/util';
import { ElNotification, type FormInstance, type FormRules } from 'element-plus'

/*============选择框============*/
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

/**
 * 查询方法
 */
const queryToService = () => {
    console.log('打印几次');

    let params: tableListParams = formInline.value
    tableApi.getList(params).then(res => {

        tableData.value = res.list
    }).catch(error => {
        console.log(error)
    })
}

/* 重置方法 */
function resetForm() {
    formInline.value = {
        ai_name: '',
        ai_status: '',
        use_date: '',
        page: 1,
        pageSize: 10
    }
    debouncedSearch()
}


/*===========编辑部分=============*/
/* 表格验证部分 */
const ruleFormRef = ref<FormInstance>()

const rules = reactive<FormRules<UpdateTableDTO>>({
    ai_name: [
        { required: true, message: '请输入模型名称', trigger: 'blur' },
        { min: 3, message: '最少需要三个字', trigger: 'blur' },
    ],
    ai_status: [
        { required: true, message: '请选择模型状态', trigger: 'blur' },
    ],
    ai_id: [
        { required: true, message: '请输入模型ID', trigger: 'blur' },
    ],
    remark: [
        { required: true, message: '请输入描述', trigger: 'blur' }
    ]
})

const dialogFormVisible = ref(false)

let dialogForm = reactive<UpdateTableDTO>({
    ai_id: 0,
    ai_name: '',
    remark: '',
    ai_use: 0,
    ai_status: ''
})

/**
 * 点击编辑按钮 赋值
 * @param params 
 */
const edit = (params: tableDTO) => {
    const { ai_id, ai_name, remark, ai_use, ai_status } = params

    // 逐个赋值，保持 reactive 对象引用不变
    dialogForm.ai_id = ai_id
    dialogForm.ai_name = ai_name
    dialogForm.remark = remark
    dialogForm.ai_use = ai_use
    dialogForm.ai_status = ai_status

    dialogFormVisible.value = true
}

const submit = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate(async (valid, fields) => {
        if (valid) {
            dialogFormVisible.value = false

            const res = await tableApi.update(dialogForm)

            ElNotification({
                title: '成功',
                message: res.message,
                type: 'success',
            })

            debouncedSearch()
        } else {
            console.log('error submit!', fields)
        }
    })
}

/*============方法处理部分 对于防抖以及初始化============*/

const debouncedSearch = debounce(queryToService, 500)

onMounted(() => {
    debouncedSearch()
})


</script>

<style lang="scss" scoped>
.con-page {
    flex-direction: column;
}
</style>
