<template>
    <div class="con-page">
        <div>
            <el-button type="primary" @click="create_data">创建数据</el-button>
        </div>

    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue';
import { tableApi, type tableListParams, type tableDTO, type UpdateTableDTO } from '@/api/table';
import { debounce, throttle } from '@/utils/util';
import { ElNotification, type FormInstance, type FormRules } from 'element-plus'
import { boardApi } from './type'

/*============选择框============*/
const create_data = async () => {
    try {
        const response = await boardApi.faker_sql_data()
    } catch (error) {
        console.log(error);
    }
}


</script>

<style lang="scss" scoped>
.con-page {
    flex-direction: column;
}
</style>
