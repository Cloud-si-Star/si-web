<template>
    <div class="con-page alone-set">
        <div class="query-position">
            <el-form :inline="true" :model="formInline">
                <el-form-item label="添加ID">
                    <el-input v-model="formInline.ai_id"/>
                </el-form-item>
                <el-form-item label="添加ID">
                    <el-input v-model="formInline.ai_id"/>
                </el-form-item>
                <el-form-item label="添加ID">
                    <el-input v-model="formInline.ai_id"/>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="queryParams">查 询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="btn-position">
            <el-button type="primary">导 出</el-button>
        </div>
        <div class="table-position">
            <el-table
                :data="tableAiData"
                border
            >
                <el-table-column prop="ai_id" label="AI_ID"></el-table-column>
                <el-table-column prop="ai_name" label="AI_ID"></el-table-column>
                <el-table-column prop="ai_use" label="AI_ID"></el-table-column>
                <el-table-column fixed="right" label="Operations" min-width="120">
                <template #default="scope">
                    <el-button link type="primary" size="small" @click="handleClick(scope.row)">
                    Detail
                    </el-button>
                    <el-button link type="primary" size="small">Edit</el-button>
                </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script setup lang="ts">
import {useAiStore, type ai_item } from '@/stores/ai_item.ts'
import {ref} from 'vue'
import { userApi, type User } from '@/api/user'
const users = ref<User[]>([])


const formInline =ref<{
    ai_id:number
}>({
    ai_id:10001
})

const user_ai_store=useAiStore()

const tableAiData = user_ai_store.aiTable

const handleClick = (params:ai_item)=>{
    const copyItem = {...params}
    copyItem.ai_use = 2000
    user_ai_store.addAiItem(copyItem)
}

const queryParams=async ()=>{
    
}

</script>

<style lang="scss" scoped>
.alone-set{
    flex-direction: column;
}
</style>