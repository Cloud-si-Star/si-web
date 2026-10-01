<template>
    <div class="con-page alone-set">
        <div class="table-content">
            <div class="query-box">
                <el-form :inline="true" :model="queryForm">
                    <el-form-item label="文件名称">
                        <el-input v-model="queryForm.fileName" />
                    </el-form-item>
                    <el-form-item label="文件类型" style="width: 240px">
                        <el-select v-model="queryForm.fileType">
                            <el-option value="1" label="img"></el-option>
                            <el-option value="2" label="zip"></el-option>
                            <el-option value="3" label="pdf"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button type="primary" @click="query">查 询</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <div class="table-box">
                <el-table :data="tabelData" style="height: 100%;" border align="center" header-align="center">
                    <el-table-column label="序号" type="index" width="60"></el-table-column>
                    <el-table-column label="文件名称" prop="fileName" show-overflow-tooltip></el-table-column>
                    <el-table-column label="文件类型" prop="fileType" width="100"></el-table-column>
                    <el-table-column label="文件大小" prop="fileSize" width="100"
                        :formatter="formatFileSize"></el-table-column>
                    <el-table-column label="上传用户" prop="uploadUser" width="100"></el-table-column>
                    <el-table-column label="上传时间" prop="uploadTime"></el-table-column>

                    <el-table-column label="文件描述" prop="remark" width="150" show-overflow-tooltip></el-table-column>
                    <el-table-column label="操 作" width="150" fixed="right">
                        <template #default="scope">
                            <el-button link type="primary" @click="downlaod(scope.row.id)">下 载</el-button>
                            <el-button link type="danger">删 除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <el-pagination class="table-pagination" :current-page="queryForm.page" :page-size="queryForm.pageSize"
                :page-sizes="[5, 10, 20, 50, 100]" :total="total" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handleCurrentChange" @size-change="handleSizeChange" />
        </div>
        <div class="upload-page">
            <div class="title-content">文件上传</div>
            <el-upload class="avatar-uploader" :auto-upload="false" :show-file-list="false" :on-change="handleChange">
                <div class="upload-wrapper">
                    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                </div>
            </el-upload>

            <div class="upload-list">
                <transition-group name="file-item">
                    <div class="upload-item" v-for="(value, index) in fileReadyList" :key="value.uid">
                        <!-- 序号 -->
                        <span class="file-index">{{ index + 1 }}</span>

                        <!-- 文件名称 + tooltip 悬浮展示全名 -->
                        <el-tooltip :content="value.name" effect="dark" placement="top" :show-after="300">
                            <span class="file-content">{{ value.name }}</span>
                        </el-tooltip>

                        <!-- 右侧图标组，整体居右 -->
                        <div class="file-action">
                            <el-icon class="icon-close" @click="removeItem(value.uid)">
                                <CloseBold />
                            </el-icon>
                            <el-icon class="icon-upload" @click="hanleFile(value)">
                                <Upload />
                            </el-icon>
                        </div>
                    </div>
                </transition-group>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { tableApi } from '@/api/table';
import { onMounted, ref } from 'vue'
import { ElNotification } from 'element-plus'
import type { UploadProps, UploadFile } from 'element-plus'
import { fileApi, formatFileSize, type FileItem, type queryFile } from '.';
import { downloadBlobFile, getFileNameFromHeader } from '@/utils/util';


/* ===========查询域 and 表格域=========== */
const queryForm = ref<queryFile>({
    fileName: '',
    fileType: '',
    page: 1,
    pageSize: 10
})

const tabelData = ref<FileItem[]>([])
const total = ref(0)

const query = async () => {
    try {
        const response = await fileApi.getFiles({})
        tabelData.value = response.list
        total.value = response.total
    } catch (err) {
        console.log(err);
        tabelData.value = []
        total.value = 0
    }

}

onMounted(() => {
    query()
})

/** 切换页码时更新当前页。 */
const handleCurrentChange = (page: number): void => {
    queryForm.value.page = page
    query()
}

/** 改变每页条数后回到第一页，避免当前页超出新页数范围。 */
const handleSizeChange = (pageSize: number): void => {
    queryForm.value.pageSize = pageSize
    queryForm.value.page = 1
    query()
}

const downlaod = async (id: number) => {
    try {

        const response = await fileApi.downloadBlobFile(id)

        const disposition = String(
            response.headers?.['content-disposition'] ?? ''
        )

        const fileName = getFileNameFromHeader(disposition) || '未命名文件'

        downloadBlobFile(response.data, fileName)


    } catch (err) {
        console.log(err);
    }
}

/* ===========文件上传部分=========== */

const fileValue = ref<File>()

const fileReadyList = ref<UploadFile[]>([])


const handleChange: UploadProps['onChange'] = (uploadFile) => {
    fileReadyList.value.push(uploadFile)
}

/**
 * 移除不需要上传的文件
 */
const removeItem = (uid: number) => {

    fileReadyList.value = fileReadyList.value.filter(e => e.uid != uid)

}

const hanleFile = async (params: UploadFile) => {
    try {
        const res = await tableApi.upload(params.raw!)
        if (res.code == 0) {
            ElNotification({
                title: '成功',
                type: 'success',
                message: res.message,
                duration: 6000,
            })
            removeItem(params.uid)
        }
    } catch (err) {

        console.log(err);
    } finally {
        query()
    }


}

</script>

<style lang="scss" scoped>
.upload-page {
    width: 320px;
    margin-left: 10px;
    border: 3px dashed #dfdff5;
    border-radius: 7px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #f4f4ff;

    .title-content {
        height: 40px;
        width: 100%;
        line-height: 40px;
        font-weight: 600;
        text-align: left;
        padding-left: 20px;
        background: #FFF;
    }

    .avatar-uploader {
        width: 300px;
        height: 120px;
        border: 1px solid;
        text-align: center;
        line-height: 120px;
        background: #FFF;
        border: 1px dashed #f4f4ff;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 45px;
        color: #a394ea;

        :deep(.el-upload) {
            width: 100%;
            height: 100%;

            .upload-wrapper {
                height: 100%;
                width: 100%;
            }
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


.upload-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 300px;
}

.upload-item {
    display: flex;
    align-items: center;
    gap: 14px;
    width: 100%;
    /* 加大内边距，高度拉高，不再短小 */
    padding: 14px 18px;
    border-radius: 10px;
    /* 默认背景色，不是纯白 */
    background-color: #FFF;
    border: 1px solid transparent;
    transition: all 0.24s ease;
}

.file-index {
    flex: 0 0 28px;
    color: #606266;
    text-align: center;
    font-size: 15px;
}

.file-content {
    flex: 1;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: #303133;
    font-size: 15px;
}

.file-action {
    flex: 0 0 auto;
    display: flex;
    gap: 16px;
}

.icon-close {
    font-size: 18px;
    color: #909399;
    cursor: pointer;
    transition: color 0.2s;

    &:hover {
        color: #f56c6c;
    }
}

.icon-upload {
    font-size: 18px;
    color: #909399;
    cursor: pointer;
    transition: color 0.2s;

    &:hover {
        color: #7b61ff;
    }
}

/* transition-group 动画class */
.file-item-enter-from,
.file-item-leave-to {
    opacity: 0;
    transform: translateX(-12px);
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    margin-top: 0;
    margin-bottom: 0;
}

.file-item-enter-active,
.file-item-leave-active {
    transition: all 0.24s ease;
}
</style>