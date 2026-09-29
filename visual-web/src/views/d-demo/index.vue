<template>
    <div class="con-page alone-set">
        <div class="table-content">
            <div class="query-box">
                <el-form :inline="true" :model="queryForm">
                    <el-form-item label="文件名称">
                        <el-input v-model="queryForm.name" />
                    </el-form-item>
                    <el-form-item label="文件类型" style="width: 240px">
                        <el-select>
                            <el-option value="1" label="img"></el-option>
                            <el-option value="2" label="zip"></el-option>
                            <el-option value="3" label="pdf"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button type="primary">查 询</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <div class="table-box">
                <el-table :data="paginatedTableData" style="height: 100%;" border align="center" header-align="center">
                    <el-table-column label="序号" type="index" :index="getRowIndex" width="100"></el-table-column>
                    <el-table-column label="文件名称" prop="name"></el-table-column>
                    <el-table-column label="文件类型" prop="type"></el-table-column>
                    <el-table-column label="文件描述" prop="remark"></el-table-column>
                </el-table>
            </div>
            <el-pagination class="table-pagination" :current-page="pagination.currentPage"
                :page-size="pagination.pageSize" :page-sizes="[2, 5, 10, 20]" :total="tableData.length"
                layout="total, sizes, prev, pager, next, jumper" @current-change="handleCurrentChange"
                @size-change="handleSizeChange" />
        </div>
        <div class="upload-page">
            <div class="title-content">文件上传</div>
            <el-upload class="avatar-uploader" :auto-upload="false" :show-file-list="false"
                :on-change="beforeAvatarUpload">
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            </el-upload>
            <el-button type="primary" @click="hanleFile">上 传</el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { tableApi } from '@/api/table';
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadProps } from 'element-plus'

/** 当前页面展示的文件记录。 */
interface FileRecord {
    name: string
    type: number
    remark: string
}

/** 本地分页使用的页码与每页条数。 */
interface PaginationState {
    currentPage: number
    pageSize: number
}

/* ===========查询域=========== */
const queryForm = {
    name: '',
    type: 0
}

/* ===========表格域=========== */
const tableData: FileRecord[] = [
    {
        name: '前端开发简历.pdf',
        type: 3,
        remark: '这是我的职业简历'
    },
    {
        name: 'offer.img',
        type: 1,
        remark: '这是我收到的高薪offer'
    },
    {
        name: '前端开发简历.pdf',
        type: 3,
        remark: '这是我的职业简历'
    },
    {
        name: '前端开发简历.pdf',
        type: 3,
        remark: '这是我的职业简历'
    },
    {
        name: '前端开发简历.pdf',
        type: 3,
        remark: '这是我的职业简历'
    },
]

const pagination = ref<PaginationState>({
    currentPage: 1,
    pageSize: 2
})

/** 根据当前页码和每页条数，截取表格需要显示的数据。 */
const paginatedTableData = computed(() => {
    const startIndex = (pagination.value.currentPage - 1) * pagination.value.pageSize
    return tableData.slice(startIndex, startIndex + pagination.value.pageSize)
})

/** 切换页码时更新当前页。 */
const handleCurrentChange = (page: number): void => {
    pagination.value.currentPage = page
}

/** 改变每页条数后回到第一页，避免当前页超出新页数范围。 */
const handleSizeChange = (pageSize: number): void => {
    pagination.value.pageSize = pageSize
    pagination.value.currentPage = 1
}

/** 让序号在不同分页之间保持连续。 */
const getRowIndex = (index: number): number => {
    return (pagination.value.currentPage - 1) * pagination.value.pageSize + index + 1
}










const imageUrl = ref('')

const fileValue = ref<File>()

const handleAvatarSuccess: UploadProps['onSuccess'] = (
    response,
    uploadFile
) => {
    imageUrl.value = URL.createObjectURL(uploadFile.raw!)
}


const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
    console.log(rawFile);
    fileValue.value = rawFile.raw
    return true

    if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('Avatar picture must be JPG format!')
        return false
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!')
        return false
    }
    return true
}

const hanleFile = () => {

    tableApi.upload(fileValue.value!)
}

</script>

<style lang="scss" scoped>
.upload-page {
    width: 240px;
    margin-left: 10px;
    border: 3px dashed #dfdff5;
    border-radius: 7px;

    display: flex;
    flex-direction: column;
    align-items: center;

    .title-content {

        height: 40px;
        width: 100%;
        line-height: 40px;
        font-weight: 600;
        text-align: left;
        padding-left: 20px;
    }

    .avatar-uploader {
        width: 200px;
        height: 120px;
        border: 1px solid;
        text-align: center;
        line-height: 120px;
        background: #f4f4ff;
        border: 1px dashed #f4f4ff;
        border-radius: 5px;

        &:hover {
            cursor: pointer;
        }
    }
}

.table-content {
    flex: 1;
    display: flex;
    flex-direction: column;

    .table-pagination {
        flex-shrink: 0;
        justify-content: flex-end;
        padding: 12px 0 0;
    }

    .table-box {
        flex: 1;
        overflow: hidden;
    }
}
</style>