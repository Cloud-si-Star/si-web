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
