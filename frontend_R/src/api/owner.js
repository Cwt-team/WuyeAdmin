import { request } from '../utils/request'

// 业主信息API接口
export default {
  // 获取业主列表
  getOwnerList(params) {
    return request.get('/owners', params)
  },
  
  // 获取业主详情
  getOwnerDetail(id) {
    return request.get(`/owners/${id}`)
  },
  
  // 获取业主权限
  getOwnerPermission(id) {
    return request.get(`/owners/${id}/permission`)
  },
  
  // 添加业主
  createOwner(data) {
    // 适配后端API格式
    const payload = {
      communityId: data.communityId,
      houseId: data.houseId,
      name: data.name,
      gender: data.gender,
      phoneNumber: data.phoneNumber || data.phone,
      idCard: data.idCard,
      email: data.email || '',
      city: data.city || '',
      address: data.address || '',
      ownerType: data.ownerType || '业主',
      remark: data.remark || ''
    }
    return request.post('/owners', payload)
  },
  
  // 更新业主
  updateOwner(id, data) {
    // 适配后端API格式
    const payload = {}
    
    // 只包含实际修改的字段
    if (data.name !== undefined) payload.name = data.name
    if (data.gender !== undefined) payload.gender = data.gender
    if (data.phoneNumber !== undefined) payload.phoneNumber = data.phoneNumber
    if (data.phone !== undefined) payload.phoneNumber = data.phone
    if (data.idCard !== undefined) payload.idCard = data.idCard
    if (data.email !== undefined) payload.email = data.email
    if (data.city !== undefined) payload.city = data.city
    if (data.address !== undefined) payload.address = data.address
    if (data.ownerType !== undefined) payload.ownerType = data.ownerType
    if (data.communityId !== undefined) payload.communityId = data.communityId
    if (data.houseId !== undefined) payload.houseId = data.houseId
    if (data.remark !== undefined) payload.remark = data.remark
    
    return request.put(`/owners/${id}`, payload)
  },
  
  // 删除业主
  deleteOwner(id) {
    return request.delete(`/owners/${id}`)
  },
  
  // 更新业主权限
  updateOwnerPermission(id, data) {
    return request.put(`/owners/${id}/permission`, data)
  },
  
  // 导出业主信息
  exportOwners(params) {
    return request.get('/owners/export', params)
  },
  
  // 导出业主信息模板
  exportOwnerTemplate() {
    return request.get('/owners/export-template')
  },
  
  // 导入业主信息
  importOwners(formData) {
    return request.post('/owners/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
} 