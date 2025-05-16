import { request } from '../utils/request'

// 房屋信息API接口
export default {
  // 获取房屋列表
  getHouseList(params) {
    return request.get('/houses', params)
  },
  
  // 获取房屋详情
  getHouseDetail(id) {
    return request.get(`/houses/${id}`)
  },
  
  // 获取房屋树形结构
  getHouseTree(communityId) {
    return request.get(`/houses/tree/${communityId}`)
  },
  
  // 获取社区房屋的统计信息
  getHouseStats(communityId) {
    return request.get(`/houses/stats/${communityId}`)
  },
  
  // 获取社区下的房屋选项
  getHouseOptions(communityId) {
    // 获取房屋列表，筛选出房间级别的房屋作为选项
    return request.get('/houses', {
      communityId: communityId,
      pageSize: 1000, // 获取足够多的房屋
      level: 4 // 只获取房间级别的房屋
    })
  },
  
  // 添加房屋
  createHouse(data) {
    // 构建API参数
    const payload = {
      communityId: data.communityId,
      parentId: data.parentId,
      level: data.level,
      districtNumber: data.districtNumber || '',
      buildingNumber: data.buildingCode || '',
      unitNumber: data.unitNumber || '',
      roomNumber: data.roomNumber || '',
      houseArea: data.houseArea || 0,
      houseUnit: data.houseUnit || '',
      ownerName: data.ownerName || '',
      status: data.status || '未入住',
      fullName: data.fullName || '',
      remark: data.remark || ''
    }
    
    return request.post('/houses', payload)
  },
  
  // 更新房屋
  updateHouse(id, data) {
    // 构建API参数
    const payload = {
      communityId: data.communityId,
      buildingNumber: data.buildingCode || '',
      houseUnit: data.houseUnit || '',
      ownerName: data.ownerName || '',
      status: data.status || '未入住',
      remark: data.remark || ''
    }
    
    // 根据房屋层级添加对应字段
    if (data.houseArea) payload.houseArea = data.houseArea
    
    return request.put(`/houses/${id}`, payload)
  },
  
  // 删除房屋
  deleteHouse(id) {
    return request.delete(`/houses/${id}`)
  },
  
  // 将后端返回的数据转换为前端表格所需格式
  transformHouseData(item) {
    return {
      id: item.id,
      communityId: item.communityId,
      communityName: item.communityName,
      parentId: item.parentId,
      level: item.level,
      districtNumber: item.districtNumber || '',
      buildingCode: item.buildingNumber || '',
      houseCode: item.houseCode || item.roomNumber || '',
      unitNumber: item.unitNumber || '',
      roomNumber: item.roomNumber || '',
      houseArea: item.houseArea || 0,
      houseUnit: item.houseUnit || '',
      ownerName: item.ownerName || '',
      status: item.status || '未入住',
      fullName: item.fullName || '',
      remark: item.remark || ''
    }
  }
} 