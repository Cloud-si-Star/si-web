import axios, {
    type AxiosInstance,
    type AxiosRequestConfig,
    type AxiosResponse,
    type InternalAxiosRequestConfig,
} from 'axios'
import { config } from '@/utils/config'
import type { ApiResponse } from '@/types/types.ts'

/**
 * 创建 Axios 实例
 * 统一配置 baseURL、超时、请求头
 */
const instance: AxiosInstance = axios.create({
    baseURL: config.baseURL,
    timeout: config.timeout,
    headers: {
        'Content-Type': 'application/json',
    },
})

/**
 * 请求拦截器
 * 作用：自动携带 token、统一加时间戳等
 */
instance.interceptors.request.use(
    (reqConfig: InternalAxiosRequestConfig) => {
        // 从 localStorage 取 token，有就带上
        const token = localStorage.getItem('token')
        if (token && reqConfig.headers) {
            reqConfig.headers.Authorization = `Bearer ${token}`
        }
        return reqConfig
    },
    (error) => {
        return Promise.reject(error)
    }
)

/**
 * 响应拦截器
 * 作用：剥掉外层 { code, message, data }，直接返回 data
 *       统一处理业务错误和 HTTP 错误
 */
instance.interceptors.response.use(
    (response) => {
        const res = response.data

        return response

        // 如果后端没有按 { code, message, data } 返回，直接放行
        if (res.code === undefined) {
            return response.data
        }

        // 业务成功
        if (res.code === config.successCode) {
            return res.data
        }

        // 业务失败：弹出提示并 reject
        console.error(`[业务错误] ${res.code}: ${res.message}`)
        return Promise.reject(new Error(res.message || '请求失败'))
    },
    (error) => {
        // HTTP 层错误处理
        let message = '网络异常，请稍后重试'
        console.log('这里没有');

        if (error.response) {
            const status = error.response.status
            const statusMap: Record<number, string> = {
                400: '请求参数错误',
                401: '登录已过期，请重新登录',
                403: '没有权限访问',
                404: '请求的资源不存在',
                500: '服务器内部错误',
                502: '网关错误',
                503: '服务不可用',
            }
            message = statusMap[status] || `请求失败 (${status})`

            // 401 特殊处理：清除 token 并跳转登录
            if (status === 401) {
                localStorage.removeItem('token')
                // router.push('/login')  // 有路由的话取消注释
            }
        } else if (error.code === 'ECONNABORTED') {
            message = '请求超时，请检查网络'
        }

        console.error(`[HTTP 错误] ${message}`, error)
        return Promise.reject(new Error(message))
    }
)

/**
 * 对外暴露的请求方法
 * 泛型 T 表示后端 data 字段的类型
 */
export const request = {
    get<T = unknown>(url: string, params?: object, cfg?: AxiosRequestConfig) {
        return instance.get<T, T>(url, { params, ...cfg })
    },

    post<T = unknown>(url: string, data?: object, cfg?: AxiosRequestConfig) {
        return instance.post<T, T>(url, data, cfg)
    },

    put<T = unknown>(url: string, data?: object, cfg?: AxiosRequestConfig) {
        return instance.put<T, T>(url, data, cfg)
    },

    delete<T = unknown>(url: string, params?: object, cfg?: AxiosRequestConfig) {
        return instance.delete<T, T>(url, { params, ...cfg })
    },

    patch<T = unknown>(url: string, data?: object, cfg?: AxiosRequestConfig) {
        return instance.patch<T, T>(url, data, cfg)
    },
}

export default instance