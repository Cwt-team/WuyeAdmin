import { request } from '../utils/request'

// 门禁设备API接口
export default {
  // 获取门禁设备列表
  getDeviceList(params) {
    return request.get('/sip/devices', params)
  },
  
  // 获取门禁设备详情
  getDeviceDetail(id) {
    return request.get(`/sip/device/${id}`)
  },
  
  // 添加门禁设备
  createDevice(data) {
    // 适配后端API格式
    const payload = {
      communityId: data.communityId,
      deviceCode: data.deviceCode,
      deviceSn: data.deviceSn || '',
      name: data.name || '',
      softVer: data.softVer || '',
      deviceType: data.deviceType || '门口机',
      status: data.status || '离线'
    }
    return request.post('/sip/device', payload)
  },
  
  // 更新门禁设备
  updateDevice(id, data) {
    const payload = {
      id: id,
      ...data
    }
    return request.post('/sip/device', payload)
  },
  
  // 删除门禁设备
  deleteDevice(id) {
    return request.delete(`/sip/device/${id}`)
  },
  
  // 获取设备类型列表
  getDeviceTypes() {
    return Promise.resolve({
      success: true,
      data: [
        { value: '门口机', label: '门口机' },
        { value: '围栏机', label: '围栏机' },
        { value: '人脸识别机', label: '人脸识别机' },
        { value: '其他', label: '其他' }
      ]
    })
  },
  
  // 远程开门
  remoteOpenDoor(deviceCode, communityId) {
    return request.post(`/sip/oneLock`, {
      deviceCode,
      communityId
    })
  },
  
  // 获取设备照片记录
  getDevicePhotos(deviceId) {
    return request.get(`/sip/device/${deviceId}/photos`)
  },
  
  // 添加设备SIP配置
  addSipConfig(data) {
    return request.post('/sip/config', data)
  },
  
  // 获取SIP配置列表
  getSipConfigs(params) {
    return request.get('/sip/configs', params)
  },
  
  // 更新SIP配置
  updateSipConfig(id, data) {
    const payload = {
      id: id,
      ...data
    }
    return request.post('/sip/config', payload)
  },
  
  // 删除SIP配置
  deleteSipConfig(id) {
    return request.delete(`/sip/config/${id}`)
  }
} 