import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios'

/**
 * API基础配置
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = 15000 // 15秒超时

/**
 * 创建axios实例
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 请求拦截器
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 可以在这里添加token等认证信息
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error: AxiosError) => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`[API Response] ${response.config.url}`, response.status)
    return response.data
  },
  (error: AxiosError) => {
    // 统一错误处理
    if (error.response) {
      // 服务器返回错误响应
      const status = error.response.status
      const data = error.response.data as any
      
      switch (status) {
        case 400:
          console.error('[API Error 400] 请求参数错误:', data?.detail || error.message)
          throw new Error(data?.detail || '请求参数错误')
        
        case 401:
          console.error('[API Error 401] 未授权，请重新登录')
          // 可以在这里处理token过期，跳转到登录页
          throw new Error('未授权，请重新登录')
        
        case 403:
          console.error('[API Error 403] 没有权限访问')
          throw new Error('没有权限访问')
        
        case 404:
          console.error('[API Error 404] 请求的资源不存在:', error.config?.url)
          throw new Error('请求的资源不存在')
        
        case 500:
          console.error('[API Error 500] 服务器内部错误:', data?.detail || error.message)
          throw new Error(data?.detail || '服务器内部错误，请稍后重试')
        
        case 502:
        case 503:
        case 504:
          console.error(`[API Error ${status}] 服务不可用`)
          throw new Error('服务暂时不可用，请稍后重试')
        
        default:
          console.error(`[API Error ${status}]`, data?.detail || error.message)
          throw new Error(data?.detail || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('[API Error] 网络连接失败，请检查后端服务:', error.message)
      throw new Error('网络连接失败，请检查后端服务是否启动')
    } else {
      // 请求配置出错
      console.error('[API Error] 请求配置错误:', error.message)
      throw new Error('请求配置错误: ' + error.message)
    }
  }
)

/**
 * 通用GET请求
 */
export const get = <T = any>(url: string, params?: any): Promise<T> => {
  return apiClient.get(url, { params })
}

/**
 * 通用POST请求
 */
export const post = <T = any>(url: string, data?: any): Promise<T> => {
  return apiClient.post(url, data)
}

/**
 * 通用PUT请求
 */
export const put = <T = any>(url: string, data?: any): Promise<T> => {
  return apiClient.put(url, data)
}

/**
 * 通用DELETE请求
 */
export const del = <T = any>(url: string, params?: any): Promise<T> => {
  return apiClient.delete(url, { params })
}

/**
 * 导出axios实例供特殊需求使用
 */
export default apiClient