import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    return response.data
  },
  error => {
    // 对响应错误做点什么
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 获取看板数据
export const getDashboardData = () => {
  return api.get('/dashboard')
}

// 获取所有指数数据
export const getIndices = () => {
  return api.get('/indices')
}

// 获取特定指数数据
export const getIndex = (indexCode) => {
  return api.get(`/indices/${indexCode}`)
}

// 获取特定指数的核心数据
export const getIndexCoreData = (indexCode) => {
  return api.get(`/indices/${indexCode}/core_data`)
}

// 获取特定指数的历史数据
export const getIndexHistory = (indexCode) => {
  return api.get(`/indices/${indexCode}/history`)
}

// 健康检查
export const healthCheck = () => {
  return api.get('/health')
}

export default api