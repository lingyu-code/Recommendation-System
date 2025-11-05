import axios from 'axios'

// 创建axios实例
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器 - 添加JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
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

    // 认证相关 - JWT
    login(credentials) {
        return api.post('/auth/token/', credentials)
    },

    refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token')
        return api.post('/auth/token/refresh/', { refresh: refreshToken })
    },

    register(userData) {
        return api.post('/auth/register/', userData)
    },

    // 用户资料相关
    getProfile() {
        return api.get('/auth/profile/')
    },

    updateProfile(userData) {
        return api.put('/auth/profile/', userData)
    },

    // 购买相关
    purchaseProduct(purchaseData) {
        return api.post('/purchase/', purchaseData)
    },

    purchaseStock(purchaseData) {
        return api.post('/purchase/stock/', purchaseData)
    },

    getPurchaseRecords() {
        return api.get('/purchase/records/')
    },
}

export default api
