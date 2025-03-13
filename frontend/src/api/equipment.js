import axios from 'axios'

// 获取设备列表
export function getEquipmentList(params) {
    return axios({
        url: '/api/equipment',
        method: 'get',
        params
    })
}

// 添加设备
export function addEquipment(data) {
    return axios({
        url: '/api/equipment',
        method: 'post',
        data
    })
}

// 更新设备
export function updateEquipment(id, data) {
    return axios({
        url: `/api/equipment/${id}`,
        method: 'put',
        data
    })
}

// 删除设备
export function deleteEquipment(id) {
    return axios({
        url: `/api/equipment/${id}`,
        method: 'delete'
    })
}

// 检查设备网络状态
export function checkDeviceNetwork(id) {
    return axios({
        url: `/api/equipment/${id}/check-network`,
        method: 'post'
    })
}

// 检查设备状态
export function checkDeviceStatus(id) {
    return axios({
        url: `/api/equipment/${id}/check-status`,
        method: 'post'
    })
} 