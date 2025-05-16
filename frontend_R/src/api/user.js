import { request } from '../utils/request'

// 用户API接口
export default {
  // 用户登录
  login(data) {
    return request.post('/login', data)
  },
  
  // 获取用户信息
  getUserInfo() {
    return request.get('/user-info')
  },
  
  // 用户退出登录
  logout() {
    return request.post('/logout')
  },
  
  // 获取管理员角色列表
  getAdminRoles(params) {
    return request.get('/admin-roles', params)
  },
  
  // 获取当前用户的菜单权限
  getUserMenus() {
    return request.get('/user/menus')
  },
  
  // 修改密码
  changePassword(data) {
    return request.post('/change-password', data)
  }
} 