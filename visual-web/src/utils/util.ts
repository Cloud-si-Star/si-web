/**
 * 防抖函数 制定一个时间 触发函数 重置时间 如果没有重置就执行fn
 * @param fn 需要防抖的函数
 * @param delay 等待毫秒
 */
export function debounce(fn: (...args: any[]) => void, delay: number) {
    let timer: number | null = null
    return (...args: any[]) => {
        if (timer) clearTimeout(timer)

        timer = window.setTimeout(() => {
            fn(...args)
        }, delay)
    }
}


/**
 * 节流函数  无论点击多少次 只有在固定时间内才会执行原有函数
 * @param fn  需要防抖的函数
 * @param interval 执行时间
 * @returns 
 */
export function throttle(fn: (...args: any[]) => void, interval: number) {
    let lastTime = 0
    return (...args: any[]) => {
        const nowTime = Date.now()

        if (nowTime - lastTime >= interval) {
            lastTime = nowTime
            fn(...args)
        }
    }
}


/**
 * 下载blob文件
 * @param blob 后端返回blob对象
 * @param fileName 文件名（后端返回的文件名，或者自己传）
 */
export function downloadBlobFile(blob: Blob, fileName: string) {
    // 创建blob地址
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName // 下载后的文件名
    document.body.appendChild(a)
    a.click()
    // 释放内存，清理dom
    a.remove()
    URL.revokeObjectURL(url)
}

/**
 * 解析响应头获取文件名工具
 * @param headerStr 响应头传过来的参数
 * @returns 
 */
export function getFileNameFromHeader(headerStr: string) {
    if (!headerStr) return ''
    // 匹配 filename=xxx 或者 filename*=utf-8''xxx
    const reg = /filename\*?=utf-8''"?([^;"]+)/
    const match = headerStr.match(reg)
    if (match && match[1]) {
        return decodeURIComponent(match[1])
    }
    return ''
}