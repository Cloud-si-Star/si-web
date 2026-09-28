<template>
    <div class="con-page alone-set">
        <div class="table-content">


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
import { tableApi, type tableListParams, type tableDTO, type UpdateTableDTO } from '@/api/table';
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { UploadProps } from 'element-plus'

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
    fileValue.value = rawFile
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
}
</style>