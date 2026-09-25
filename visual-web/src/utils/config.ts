export const config = {
    baseURL: import.meta.env.VITE_API_BASE_URL as string,
    timeout: 30000,
    successCode: 0
} as const