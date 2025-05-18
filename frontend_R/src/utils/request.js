import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 创建axios实例
const service = axios.create({
  baseURL: '/api', // API基础路径
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从本地存储中获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 为调试添加日志
    console.log('API原始响应:', res)
    
    // 处理不同的响应格式
    
    // 1. 后端可能返回 success 字段为true的标准格式
    if (res.success === true) {
      return res
    }
    
    // 2. 后端可能返回 code 字段
    if (res.code === 0) {
      return {
        success: true,
        data: res.data || res
      }
    }
    
    // 3. 后端可能返回直接包含业主数据的结构
    if (res.owners && Array.isArray(res.owners)) {
      console.log('检测到业主数据结构:', res)
      // 直接返回原始数据，不做额外包装
      return res
    }
    
    // 3.1 后端可能没有错误状态标记，但有数据(items/list等)
    if (res.items) {
      // 后端直接返回了items数组和total，这里不做额外包装，让前端组件自己处理
      return res
    }
    
    if (res.list || res.devices || res.total !== undefined) {
      return {
        success: true,
        data: res
      }
    }
    
    // 4. 后端可能直接返回数据数组
    if (Array.isArray(res)) {
      return {
        success: true,
        data: {
          list: res,
          total: res.length
        }
      }
    }
    
    // 5. 后端可能返回单个对象（详情接口）
    if (typeof res === 'object' && res !== null && !res.success && !res.code && !res.error && !res.message) {
      return {
        success: true,
        data: res
      }
    }
    
    // 如果有error或message，说明是错误响应
    if (res.error || res.message) {
      // 处理异常情况
      const errorMsg = res.message || res.error || '请求发生错误'
      ElMessage.error(errorMsg)
      
      // 处理特定错误码
      if (res.code === 401 || res.status === 401) {
        // 未授权，清除token并重定向到登录页
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        router.push('/login')
      }
      
      return Promise.reject(new Error(errorMsg))
    }
    
    // 其他情况，默认返回原始响应
    return res
  },
  error => {
    if (error.response) {
      // 服务器响应错误
      if (error.response.status === 401) {
        // 未授权，清除token并重定向到登录页
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        router.push('/login')
      }
      
      console.error('响应错误:', error.response.data)
      ElMessage.error(error.response.data?.message || error.response.data?.error || `请求失败: ${error.response.status}`)
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.error('请求无响应:', error.request)
      ElMessage.error('服务器无响应，请检查网络连接')
    } else {
      // 请求配置错误
      console.error('请求配置错误:', error.message)
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

// API请求方法
export const request = {
  get(url, params, config = {}) {
    return service({
      url,
      method: 'get',
      params,
      ...config
    })
  },
  post(url, data, config = {}) {
    return service({
      url,
      method: 'post',
      data,
      ...config
    })
  },
  put(url, data, config = {}) {
    return service({
      url,
      method: 'put',
      data,
      ...config
    })
  },
  delete(url, params, config = {}) {
    return service({
      url,
      method: 'delete',
      params,
      ...config
    })
  },
  upload(url, formData, config = {}) {
    return service.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    })
  },
  download(url, params, config = {}) {
    return service({
      url,
      method: 'get',
      params,
      responseType: 'blob',
      ...config
    })
  }
}

export default service 