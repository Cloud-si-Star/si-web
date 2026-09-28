// src/types/axios.d.ts
import type { AxiosRequestConfig, AxiosResponse } from 'axios'

/** 后端统一响应结构 */
export interface ApiResult<T = unknown> {
    code: number
    message: string
    data: T
}

/*
declare module 'axios' {
    export interface AxiosInstance {
        request<T = any>(config: AxiosRequestConfig): Promise<T>
        get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
        delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
        head<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
        post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
        put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
        patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
    }
}
*/