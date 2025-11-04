import axios from 'axios'

// 创建axios实例
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        // 可以在这里添加token等认证信息
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 响应拦截器
api.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        console.error('API Error:', error)
        return Promise.reject(error)
    }
)

// API接口定义 - 更新为匹配后端实际URLs
export const apiService = {
    // 仪表板数据
    getDashboardData() {
        return api.get('/dashboard/')
    },

    // 获取推荐
    getRecommendations(userData) {
        return api.post('/recommendations/', userData)
    },

    // 基金相关
    getFunds(params = {}) {
        return api.get('/funds/', { params })
    },

    // 股票相关
    getStocks(params = {}) {
        return api.get('/stocks/', { params })
    },

    // 保险相关
    getInsuranceProducts(params = {}) {
        return api.get('/insurance/', { params })
    },

    // 股票日数据
    getStockDailyData() {
        return api.get('/stock-data/')
    },

    // 健康检查
    healthCheck() {
        return api.get('/health/')
    }
}

export default api
