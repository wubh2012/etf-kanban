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

/**
 * 获取看板数据
 * @param {boolean} refreshRealtime - 是否获取实时数据
 * @returns {Promise} 看板数据
 */
export const getDashboardData = (refreshRealtime = false) => {
  const params = refreshRealtime ? '?refresh=true' : '';
  return api.get(`/dashboard${params}`);
};

// 获取所有指数数据
export const getIndices = () => {
  return api.get('/indices')
}

// 获取特定指数数据
export const getIndex = (indexCode) => {
  return api.get(`/indices/${indexCode}`)
}

// 获取特定指数的历史数据
export const getIndexHistory = (indexCode) => {
  return api.get(`/indices/${indexCode}/history`)
}

// 健康检查
export const healthCheck = () => {
  return api.get('/health')
}

// 数据维护相关API
// 指数管理
export const createIndex = (data) => {
  return api.post('/indices', data)
}

export const updateIndex = (indexCode, data) => {
  return api.put(`/indices/${indexCode}`, data)
}

export const deleteIndex = (indexCode) => {
  return api.delete(`/indices/${indexCode}`)
}

// 历史数据管理
export const createHistory = (indexCode, data) => {
  return api.post(`/indices/${indexCode}/history`, data)
}

export const updateHistory = (indexCode, historyType, data) => {
  return api.put(`/indices/${indexCode}/history/${historyType}`, data)
}

export const deleteHistory = (indexCode, historyType) => {
  return api.delete(`/indices/${indexCode}/history/${historyType}`)
}

export default api