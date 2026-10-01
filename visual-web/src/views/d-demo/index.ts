import type { PageResult, PageParams } from "@/types/types";
import { request } from "@/utils/request";
import type { AxiosResponse } from 'axios'

export interface FileItem {
    fileName: string
    fileSize: number
    fileType: string
    uploadUser: string
    uploadTime: string
    remark: string
}

export interface query {
    fileName: string
    fileType: string
}

export interface queryFile extends query, PageParams { }

export const fileApi = {
    getFiles(params: queryFile) {
        return request.get<PageResult<FileItem>>('/v1/data/files', params)
    },
    downloadBlobFile(params: number) {

        return request.get<AxiosResponse<Blob>>(`/v1/data/download/${params}`, {}, { responseType: 'blob' })
    }
}

/**
 * 文件字节转可读大小（自动转为 M/G/B）
 * @param {number} bytes 字节数
 * @returns {string} 例如: 2.34 MB
 */
export function formatFileSize(params: FileItem) {
    let bytes = params.fileSize
    if (!bytes || bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
}
