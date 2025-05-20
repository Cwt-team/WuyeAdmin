import { request } from '../utils/request'

export default {
  // 获取业主房屋绑定申请列表
  getApplicationList(params) {
    return request.get('/housing-applications', params)
  },

  // 获取单个申请详情
  getApplicationDetail(id) {
    return request.get(`/housing-applications/${id}`)
  },

  // 审批通过
  approveApplication(id) {
    return request.post(`/housing-applications/${id}/approve`)
  },

  // 审批拒绝
  rejectApplication(id, data) {
    return request.post(`/housing-applications/${id}/reject`, data)
  }
} 