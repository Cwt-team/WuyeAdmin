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
    
    // 正常返回数据
    if (res.code === 0) {
      return res
    }
    
    // 处理异常情况
    ElMessage.error(res.message || '请求发生错误')
    
    // 处理特定错误码
    if (res.code === 401) {
      // 未授权，清除token并重定向到登录页
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      router.push('/login')
    }
    
    return Promise.reject(new Error(res.message || '请求发生错误'))
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
      ElMessage.error(error.response.data.message || `请求失败: ${error.response.status}`)
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

export default service 