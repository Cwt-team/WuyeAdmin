import { request } from '../utils/request'

// 社区信息API接口
export default {
  // 获取社区列表
  getCommunityList(params) {
    // 转换前端参数名称为后端API期望的参数名称
    const apiParams = {
      page: params.page || 1,
      size: params.size || 10
    }
    
    // 关键字搜索 - 名称或编号
    if (params.keyword) {
      apiParams.keyword = params.keyword
    }
    
    // 城市搜索
    if (params.location) {
      apiParams.location = params.location
    }
    
    // 门禁卡类型
    if (params.accessCardType) {
      apiParams.accessCardType = params.accessCardType
    }
    
    // 启用状态
    if (params.isEnabled !== undefined && params.isEnabled !== '') {
      apiParams.isEnabled = params.isEnabled
    }
    
    // APP人脸录入
    if (params.appRecordFace !== undefined && params.appRecordFace !== '') {
      apiParams.appRecordFace = params.appRecordFace
    }
    
    // 记录上传
    if (params.isRecordUpload !== undefined && params.isRecordUpload !== '') {
      apiParams.isRecordUpload = params.isRecordUpload
    }
    
    // 配置同步
    if (params.isSameStep !== undefined && params.isSameStep !== '') {
      apiParams.isSameStep = params.isSameStep
    }
    
    return request.get('/communities', apiParams)
  },
  
  // 获取社区详情
  getCommunityDetail(id) {
    return request.get(`/communities/${id}`)
  },
  
  // 添加社区
  createCommunity(data) {
    // 转换数据格式，适配后端API
    const payload = {
      name: data.name,
      location: data.area,
      managerMachineCount: data.buildingCount || 0,
      indoorMachineCount: data.houseCount || 0,
      accessCardType: data.accessCardType || 'NFC',
      appRecordFace: data.appRecordFace || 1,
      isSameStep: data.isSameStep || 1,
      isRecordUpload: data.isRecordUpload || 1,
      password: data.password || '123456'
    }
    return request.post('/communities', payload)
  },
  
  // 更新社区
  updateCommunity(id, data) {
    // 转换数据格式，适配后端API
    const payload = {
      name: data.name,
      location: data.area,
      managerMachineCount: data.buildingCount || 0,
      indoorMachineCount: data.houseCount || 0
    }
    // 只包含实际修改的字段
    if (data.accessCardType) payload.accessCardType = data.accessCardType
    if (data.appRecordFace !== undefined) payload.appRecordFace = data.appRecordFace
    if (data.isSameStep !== undefined) payload.isSameStep = data.isSameStep
    if (data.isRecordUpload !== undefined) payload.isRecordUpload = data.isRecordUpload
    
    return request.put(`/communities/${id}`, payload)
  },
  
  // 删除社区
  deleteCommunity(id) {
    return request.delete(`/communities/${id}`)
  },
  
  // 将后端返回的数据转换为前端表格所需格式
  transformCommunityData(item) {
    return {
      id: item.id,
      code: item.communityNumber || item.code || '',
      name: item.communityName || item.name || '',
      area: item.communityCity || item.area || item.location || '',
      address: item.communityCity || item.address || '',  // 后端没有详细地址字段，暂时使用城市字段
      developer: item.developer || '',  // 后端没有开发商字段
      buildingCount: item.managementMachineQuantity || item.managerMachineCount || 0,
      houseCount: item.indoorMachineQuantity || item.indoorMachineCount || 0,
      createTime: item.creationTime || item.createTime || '',
      accessCardType: item.accessCardType || 'NFC',
      appRecordFace: item.appRecordFace !== undefined ? item.appRecordFace : 1,
      isSameStep: item.isSameStep !== undefined ? item.isSameStep : 1,
      isRecordUpload: item.isRecordUpload !== undefined ? item.isRecordUpload : 1,
      isEnabled: item.isEnabled !== undefined ? item.isEnabled : 1
    }
  }
} 